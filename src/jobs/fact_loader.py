from __future__ import annotations

import os
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any

import pyodbc

from src.core.base_loader import BaseLoader


@dataclass(frozen=True)
class FactTableSpec:
    table_name: str
    key_columns: tuple[str, ...]
    date_column: str


class FactLoader(BaseLoader):
    LANDING_SCHEMA = "stg_nano_v2"
    # Nợ kỹ thuật đã tách khỏi luồng FULL_LOAD Dimension:
    # DimLuotKham có bản chất incremental và sẽ được xử lý trong phạm vi Fact pipeline.
    PENDING_INCREMENTAL_DIMENSIONS: tuple[str, ...] = ("DimLuotKham",)

    FACT_SPECS: tuple[FactTableSpec, ...] = (
        FactTableSpec(
            table_name="ThuPhiDichVu",
            key_columns=("MaHoSo", "MaChiTieu", "MaPhieuDichVu"),
            date_column="NgayDenKham",
        ),
        FactTableSpec(
            table_name="ThuPhiBaoHiem",
            key_columns=("MaHoSo", "MaChiTieu", "MaPhieuDichVu"),
            date_column="NgayDenKham",
        ),
        FactTableSpec(
            table_name="ThuPhiTangGiam",
            key_columns=("MaHoSo", "MaChiTieu", "MaPhieuDichVu"),
            date_column="NgayDenKham",
        ),
    )

    def __init__(
        self,
        datamart_connection: str,
        production_connection: str,
        facility_code: str,
        facility_schema: str,
        nguon_dulieu_key: int,
        co_so_key: int,
        lookback_days: int = 3,
        batch_size: int = 10000,
    ) -> None:
        super().__init__(connection_string=datamart_connection, table_name=f"FactLoader:{facility_code}")
        self.production_connection = production_connection
        self.facility_code = facility_code
        self.facility_schema = facility_schema
        self.nguon_dulieu_key = nguon_dulieu_key
        self.co_so_key = co_so_key
        self.lookback_days = lookback_days
        self.batch_size = batch_size

    @staticmethod
    def _parse_connection_string(connection_string: str) -> dict[str, str]:
        parsed: dict[str, str] = {}
        for item in connection_string.split(";"):
            if not item or "=" not in item:
                continue
            key, value = item.split("=", 1)
            parsed[key.strip().upper()] = value.strip()
        return parsed

    @staticmethod
    def _build_bcp_auth_args(conn_parts: dict[str, str]) -> list[str]:
        if conn_parts.get("UID") and conn_parts.get("PWD"):
            return ["-U", conn_parts["UID"], "-P", conn_parts["PWD"]]
        return ["-T"]

    @staticmethod
    def _normalize_date(value: Any, fallback: date) -> date:
        if value is None:
            return fallback
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d").date()
        raise ValueError(f"Không parse được ngày từ giá trị: {value}")

    def _truncate_table(self, connection: pyodbc.Connection, schema_name: str, table_name: str) -> None:
        sql = f"TRUNCATE TABLE [{schema_name}].[{table_name}];"
        self._log(f"TRUNCATE {schema_name}.{table_name}")
        self.execute_sql_sync(connection, sql)

    def _landing_cleanup(self, connection: pyodbc.Connection) -> None:
        for spec in self.FACT_SPECS:
            self._truncate_table(connection, self.LANDING_SCHEMA, spec.table_name)

    def _run_bcp_queryout(self, query: str, output_file: str, prod_parts: dict[str, str]) -> None:
        command = [
            "bcp",
            query,
            "queryout",
            output_file,
            "-S",
            prod_parts.get("SERVER", ""),
            "-d",
            prod_parts.get("DATABASE", ""),
            *self._build_bcp_auth_args(prod_parts),
            "-w",
            "-t\t",
            "-r\n",
            "-q",
        ]
        self._log(f"BCP queryout: {' '.join(command)}")
        subprocess.run(command, check=True, shell=False)

    def _run_bcp_in(self, full_table_name: str, input_file: str, dm_parts: dict[str, str]) -> None:
        command = [
            "bcp",
            full_table_name,
            "in",
            input_file,
            "-S",
            dm_parts.get("SERVER", ""),
            "-d",
            dm_parts.get("DATABASE", ""),
            *self._build_bcp_auth_args(dm_parts),
            "-w",
            "-t\t",
            "-r\n",
            "-q",
        ]
        self._log(f"BCP in: {' '.join(command)}")
        subprocess.run(command, check=True, shell=False)

    def _copy_delta_prod_to_landing(
        self,
        connection: pyodbc.Connection,
        spec: FactTableSpec,
        lookback_date: date,
        to_date: date,
    ) -> None:
        self._truncate_table(connection, self.LANDING_SCHEMA, spec.table_name)

        prod_parts = self._parse_connection_string(self.production_connection)
        dm_parts = self._parse_connection_string(self.connection_string)

        query = (
            f"SELECT * FROM dbo.{spec.table_name} WITH (NOLOCK) "
            f"WHERE CAST({spec.date_column} AS DATE) >= '{lookback_date:%Y-%m-%d}' "
            f"AND CAST({spec.date_column} AS DATE) <= '{to_date:%Y-%m-%d}'"
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
            temp_path = tmp_file.name

        try:
            self._run_bcp_queryout(query=query, output_file=temp_path, prod_parts=prod_parts)
            self._run_bcp_in(
                full_table_name=f"{self.LANDING_SCHEMA}.{spec.table_name}",
                input_file=temp_path,
                dm_parts=dm_parts,
            )
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def _get_common_columns(
        self,
        connection: pyodbc.Connection,
        source_schema: str,
        source_table: str,
        target_schema: str,
        target_table: str,
    ) -> list[str]:
        sql = """
            SELECT s.COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS s
            INNER JOIN INFORMATION_SCHEMA.COLUMNS t
                ON s.COLUMN_NAME = t.COLUMN_NAME
               AND t.TABLE_SCHEMA = ?
               AND t.TABLE_NAME = ?
            WHERE s.TABLE_SCHEMA = ?
              AND s.TABLE_NAME = ?
            ORDER BY s.ORDINAL_POSITION;
        """
        cursor = connection.cursor()
        cursor.execute(sql, target_schema, target_table, source_schema, source_table)
        return [row[0] for row in cursor.fetchall()]

    def _build_ods_merge_sql(self, spec: FactTableSpec, common_columns: list[str], lookback_date: date, to_date: date) -> str:
        if not common_columns:
            raise ValueError(f"Không tìm thấy cột chung để MERGE ODS cho bảng {spec.table_name}")

        key_columns = [column for column in spec.key_columns if column in common_columns]
        if not key_columns:
            raise ValueError(f"Không đủ cột khóa cho MERGE ODS ở bảng {spec.table_name}")

        update_columns = [
            column
            for column in common_columns
            if column not in key_columns and column.lower() not in {"createdat", "created_at", "ngaytao"}
        ]

        on_clause = " AND ".join([f"Target.[{column}] = Source.[{column}]" for column in key_columns])
        update_clause = ",\n                ".join([f"Target.[{column}] = Source.[{column}]" for column in update_columns])
        insert_columns = ", ".join([f"[{column}]" for column in common_columns])
        insert_values = ", ".join([f"Source.[{column}]" for column in common_columns])

        return f"""
            MERGE [{self.facility_schema}].[{spec.table_name}] AS Target
            USING [{self.LANDING_SCHEMA}].[{spec.table_name}] AS Source
                ON {on_clause}
            WHEN MATCHED THEN
                UPDATE SET
                {update_clause}
            WHEN NOT MATCHED BY TARGET THEN
                INSERT ({insert_columns})
                VALUES ({insert_values})
            WHEN NOT MATCHED BY SOURCE
                 AND CAST(Target.[{spec.date_column}] AS DATE) >= CAST('{lookback_date:%Y-%m-%d}' AS DATE)
                 AND CAST(Target.[{spec.date_column}] AS DATE) <= CAST('{to_date:%Y-%m-%d}' AS DATE)
            THEN DELETE;
        """

    def _merge_landing_to_ods(self, connection: pyodbc.Connection, spec: FactTableSpec, lookback_date: date, to_date: date) -> None:
        common_columns = self._get_common_columns(
            connection=connection,
            source_schema=self.LANDING_SCHEMA,
            source_table=spec.table_name,
            target_schema=self.facility_schema,
            target_table=spec.table_name,
        )
        merge_sql = self._build_ods_merge_sql(spec, common_columns, lookback_date, to_date)
        self._log(f"MERGE Landing -> ODS cho {spec.table_name}")
        self.execute_sql_sync(connection, merge_sql)

    def _build_fact_merge_batch_sql(self, lookback_date: date, to_date: date) -> str:
        return f"""
            ;WITH src_full AS (
                SELECT
                    {self.nguon_dulieu_key} AS NguonDuLieuKey,
                    {self.co_so_key} AS CoSoKey,
                    '{self.facility_code}' AS MaCoSo,
                    dv.MaThuPhi,
                    dv.MaPhieuDichVu,
                    dv.MaHoSo,
                    dv.MaChiTieu,
                    CAST({self.nguon_dulieu_key} AS VARCHAR(10)) + ':' + dv.MaChiTieu AS MaChiTieuBK,
                    dv.NgayDenKham,
                    dv.NgayVaoMay AS NgayDoanhThu,
                    ISNULL(
                        CAST(YEAR(dv.NgayVaoMay) * 10000 + MONTH(dv.NgayVaoMay) * 100 + DAY(dv.NgayVaoMay) AS INT),
                        CAST(YEAR(dv.NgayDenKham) * 10000 + MONTH(dv.NgayDenKham) * 100 + DAY(dv.NgayDenKham) AS INT)
                    ) AS DateKey,
                    COALESCE(dv.SoLuongThucHien, dv.SoLuong, 1) AS SoLuongChuan,
                    dv.TongTien AS TongTien,
                    dv.TongTien - ISNULL(tg_agg.TongGiam, 0) + ISNULL(tg_agg.TongTang, 0) AS TongTienSauTangGiam,
                    'DV' AS LoaiHinh,
                    dv.SoHoaDon,
                    dv.DaThucHien,
                    dv.TrangThaiPhieu
                FROM [{self.facility_schema}].[ThuPhiDichVu] dv WITH (NOLOCK)
                LEFT JOIN (
                    SELECT
                        MaHoSo,
                        MaChiTieu,
                        MaPhieuDichVu,
                        SUM(SoTienGiam) AS TongGiam,
                        SUM(SoTienTang) AS TongTang
                    FROM [{self.facility_schema}].[ThuPhiTangGiam] WITH (NOLOCK)
                    WHERE DaDongTien = 1
                      AND CAST(NgayDenKham AS DATE) >= CAST('{lookback_date:%Y-%m-%d}' AS DATE)
                      AND CAST(NgayDenKham AS DATE) <= CAST('{to_date:%Y-%m-%d}' AS DATE)
                    GROUP BY MaHoSo, MaChiTieu, MaPhieuDichVu
                ) tg_agg
                    ON dv.MaHoSo = tg_agg.MaHoSo
                   AND dv.MaChiTieu = tg_agg.MaChiTieu
                   AND dv.MaPhieuDichVu = tg_agg.MaPhieuDichVu
                WHERE dv.DaDongTien = 1
                  AND dv.MaChiTieu IS NOT NULL
                  AND LTRIM(RTRIM(dv.MaChiTieu)) <> ''
                  AND CAST(dv.NgayDenKham AS DATE) >= CAST('{lookback_date:%Y-%m-%d}' AS DATE)
                  AND CAST(dv.NgayDenKham AS DATE) <= CAST('{to_date:%Y-%m-%d}' AS DATE)

                UNION ALL

                SELECT
                    {self.nguon_dulieu_key} AS NguonDuLieuKey,
                    {self.co_so_key} AS CoSoKey,
                    '{self.facility_code}' AS MaCoSo,
                    bh.MaThuPhi,
                    bh.MaPhieuDichVu,
                    bh.MaHoSo,
                    bh.MaChiTieu,
                    CAST({self.nguon_dulieu_key} AS VARCHAR(10)) + ':' + bh.MaChiTieu AS MaChiTieuBK,
                    bh.NgayDenKham,
                    bh.NgayVaoMay AS NgayDoanhThu,
                    ISNULL(
                        CAST(YEAR(bh.NgayVaoMay) * 10000 + MONTH(bh.NgayVaoMay) * 100 + DAY(bh.NgayVaoMay) AS INT),
                        CAST(YEAR(bh.NgayDenKham) * 10000 + MONTH(bh.NgayDenKham) * 100 + DAY(bh.NgayDenKham) AS INT)
                    ) AS DateKey,
                    COALESCE(bh.SoLuongThucHien, bh.SoLuong, 1) AS SoLuongChuan,
                    bh.TongTien AS TongTien,
                    bh.TongTien + ISNULL(bh.TienChenhLech, 0) AS TongTienSauTangGiam,
                    'BH' AS LoaiHinh,
                    bh.SoHoaDon,
                    NULL AS DaThucHien,
                    bh.TrangThaiPhieu
                FROM [{self.facility_schema}].[ThuPhiBaoHiem] bh WITH (NOLOCK)
                WHERE bh.DaDongTien = 1
                  AND bh.MaChiTieu IS NOT NULL
                  AND LTRIM(RTRIM(bh.MaChiTieu)) <> ''
                  AND CAST(bh.NgayDenKham AS DATE) >= CAST('{lookback_date:%Y-%m-%d}' AS DATE)
                  AND CAST(bh.NgayDenKham AS DATE) <= CAST('{to_date:%Y-%m-%d}' AS DATE)
            ),
            src_batch AS (
                SELECT TOP ({self.batch_size}) *
                FROM src_full
                ORDER BY DateKey, MaHoSo, MaChiTieu, MaPhieuDichVu
            )
            MERGE [dm].[FactThuPhiDichVu] AS Target
            USING src_batch AS Source
            ON  Target.NguonDuLieuKey = Source.NguonDuLieuKey
            AND Target.CoSoKey        = Source.CoSoKey
            AND Target.MaHoSo         = Source.MaHoSo
            AND Target.MaChiTieu      = Source.MaChiTieu
            AND Target.MaPhieuDichVu  = Source.MaPhieuDichVu
            WHEN MATCHED THEN
                UPDATE SET
                    Target.TongTien            = Source.TongTien,
                    Target.TongTienSauTangGiam = Source.TongTienSauTangGiam,
                    Target.LoaiHinh            = Source.LoaiHinh,
                    Target.SoHoaDon            = Source.SoHoaDon,
                    Target.SoLuong             = Source.SoLuongChuan,
                    Target.DoanhThu            = ISNULL(CAST(Source.TongTienSauTangGiam AS FLOAT), 0),
                    Target.DaThucHien          = Source.DaThucHien,
                    Target.TrangThaiPhieu      = Source.TrangThaiPhieu,
                    Target.NgayDenKham         = Source.NgayDenKham
            WHEN NOT MATCHED BY TARGET THEN
                INSERT (
                    NguonDuLieuKey,
                    CoSoKey,
                    DateKey,
                    LuotKhamKey,
                    BenhNhanKey,
                    DichVuKey,
                    MaCoSo,
                    MaThuPhi,
                    MaPhieuDichVu,
                    MaHoSo,
                    MaChiTieu,
                    MaChiTieuBK,
                    NgayDenKham,
                    SoLuong,
                    TongTien,
                    TongTienSauTangGiam,
                    LoaiHinh,
                    SoHoaDon,
                    DoanhThu,
                    DaThucHien,
                    TrangThaiPhieu
                )
                VALUES (
                    Source.NguonDuLieuKey,
                    Source.CoSoKey,
                    Source.DateKey,
                    ISNULL((
                        SELECT TOP 1 lk.LuotKhamKey
                        FROM dm.DimLuotKham lk WITH (NOLOCK)
                        WHERE lk.NguonDuLieuKey = Source.NguonDuLieuKey
                          AND lk.MaHoSo = Source.MaHoSo
                    ), -1),
                    ISNULL((
                        SELECT TOP 1 lk.BenhNhanKey
                        FROM dm.DimLuotKham lk WITH (NOLOCK)
                        WHERE lk.NguonDuLieuKey = Source.NguonDuLieuKey
                          AND lk.MaHoSo = Source.MaHoSo
                    ), -1),
                    ISNULL((
                        SELECT TOP 1 dv2.DichVuKey
                        FROM dm.DimDichVu dv2 WITH (NOLOCK)
                        WHERE dv2.MaChiTieuBK = Source.MaChiTieuBK
                    ), ISNULL((
                        SELECT TOP 1 dv3.DichVuKey
                        FROM dm.DimDichVu dv3 WITH (NOLOCK)
                        WHERE dv3.NguonDuLieuKey = Source.NguonDuLieuKey
                          AND dv3.MaChiTieu = Source.MaChiTieu
                    ), -1)),
                    Source.MaCoSo,
                    Source.MaThuPhi,
                    Source.MaPhieuDichVu,
                    Source.MaHoSo,
                    Source.MaChiTieu,
                    Source.MaChiTieuBK,
                    Source.NgayDenKham,
                    Source.SoLuongChuan,
                    Source.TongTien,
                    Source.TongTienSauTangGiam,
                    Source.LoaiHinh,
                    Source.SoHoaDon,
                    ISNULL(CAST(Source.TongTienSauTangGiam AS FLOAT), 0),
                    Source.DaThucHien,
                    Source.TrangThaiPhieu
                )
            WHEN NOT MATCHED BY SOURCE
                 AND CAST(Target.NgayDenKham AS DATE) >= CAST('{lookback_date:%Y-%m-%d}' AS DATE)
                 AND CAST(Target.NgayDenKham AS DATE) <= CAST('{to_date:%Y-%m-%d}' AS DATE)
                 AND Target.NguonDuLieuKey = {self.nguon_dulieu_key}
                 AND Target.MaCoSo = '{self.facility_code}'
            THEN DELETE;

            SELECT @@ROWCOUNT AS MergeAffectedRows;
        """

    def _merge_ods_to_datamart_batches(self, connection: pyodbc.Connection, lookback_date: date, to_date: date) -> None:
        self._log(
            "MERGE ODS -> Datamart theo batch TOP "
            f"{self.batch_size} cho khoảng {lookback_date} -> {to_date}"
        )

        max_loops = 500
        for loop_idx in range(1, max_loops + 1):
            sql = self._prepend_nocount(self._build_fact_merge_batch_sql(lookback_date, to_date))
            cursor = connection.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            affected = int(row[0]) if row and row[0] is not None else 0
            self._log(f"Batch {loop_idx}: affected = {affected}")

            if affected == 0:
                break
            if affected < self.batch_size:
                break
        else:
            raise RuntimeError("Vượt quá số vòng lặp batch tối đa khi MERGE FactThuPhiDichVu")

    def _execute_core(self, connection: pyodbc.Connection, *args: Any, **kwargs: Any) -> None:
        from_date_input = args[0] if len(args) > 0 else kwargs.get("from_date")
        to_date_input = args[1] if len(args) > 1 else kwargs.get("to_date")

        today = date.today()
        to_date = self._normalize_date(to_date_input, fallback=today)
        lookback_date = to_date - timedelta(days=self.lookback_days)
        _from_date = self._normalize_date(from_date_input, fallback=lookback_date)

        self._log(
            f"Luồng incremental Fact theo Lookback D-{self.lookback_days}. "
            f"to_date={to_date}, lookback_date={lookback_date}, from_date_input={_from_date}"
        )

        try:
            self._log("Dọn Landing đầu luồng")
            self._landing_cleanup(connection)

            for spec in self.FACT_SPECS:
                self._copy_delta_prod_to_landing(connection, spec, lookback_date, to_date)
                self._merge_landing_to_ods(connection, spec, lookback_date, to_date)

            self._merge_ods_to_datamart_batches(connection, lookback_date, to_date)
        finally:
            self._log("Dọn Landing cuối luồng")
            self._landing_cleanup(connection)
