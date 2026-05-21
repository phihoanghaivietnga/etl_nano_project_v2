from __future__ import annotations

import argparse
import os
from pathlib import Path

import pyodbc
import yaml


TABLES: tuple[str, ...] = (
    "ThuPhiDichVu",
    "ThuPhiBaoHiem",
    "ThuPhiTangGiam",
    "ThuPhiGoi",
    "DoThiLuc",
    "HoSoKhamBenhNgoaiTru",
)
LANDING_SCHEMA = "stg_nano_v2"
EXCLUDED_SYSTEM_COLUMNS = {"macoso", "cosokey", "nguondulieukey"}


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key and key not in os.environ:
            os.environ[key] = value


def fetch_selected_columns(connection: pyodbc.Connection, table_name: str) -> list[str]:
    sql = """
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = ?
          AND TABLE_NAME = ?
        ORDER BY ORDINAL_POSITION;
    """
    cursor = connection.cursor()
    cursor.execute(sql, LANDING_SCHEMA, table_name)

    columns: list[str] = []
    for row in cursor.fetchall():
        column_name = str(row[0]).strip()
        if not column_name:
            continue
        if column_name.lower() in EXCLUDED_SYSTEM_COLUMNS:
            continue
        columns.append(column_name)
    return columns


def build_preview_payload(connection: pyodbc.Connection) -> dict[str, dict[str, object]]:
    payload: dict[str, dict[str, object]] = {}
    for table in TABLES:
        payload[table] = {"selected_columns": fetch_selected_columns(connection, table)}
    return payload


def update_tables_yaml(tables_yaml_path: Path, payload: dict[str, dict[str, object]]) -> None:
    config = yaml.safe_load(tables_yaml_path.read_text(encoding="utf-8")) or {}
    incremental_tables = config.get("incremental_tables", {})

    for table_name, table_payload in payload.items():
        if table_name not in incremental_tables:
            continue
        incremental_tables[table_name]["selected_columns"] = table_payload["selected_columns"]

    config["incremental_tables"] = incremental_tables
    tables_yaml_path.write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Đồng bộ selected_columns từ schema stg_nano_v2 vào config/tables.yaml"
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Chỉ in preview YAML ra terminal, không ghi file",
    )
    args = parser.parse_args()

    root_dir = Path(__file__).resolve().parents[1]
    load_env_file(root_dir / "config" / ".env")
    connection_string = os.getenv("STAGING_CONNECTION_STRING", "").strip()
    if not connection_string:
        raise ValueError("Thiếu STAGING_CONNECTION_STRING trong môi trường/config/.env")

    with pyodbc.connect(connection_string, autocommit=True) as connection:
        payload = build_preview_payload(connection)

    if args.preview:
        preview = {"incremental_tables": payload}
        print(yaml.safe_dump(preview, allow_unicode=True, sort_keys=False))
        return

    update_tables_yaml(root_dir / "config" / "tables.yaml", payload)
    print("Đã cập nhật selected_columns vào config/tables.yaml")


if __name__ == "__main__":
    main()
