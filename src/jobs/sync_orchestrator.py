from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import yaml

from dotenv import load_dotenv

from src.jobs.dimension_loader import DimensionLoader
from src.jobs.fact_loader import FactLoader


@dataclass(frozen=True)
class FacilityDefinition:
    code: str
    prod_env_key: str
    schema_name: str


class SyncOrchestrator:
    def __init__(
        self,
        datamart_env_key: str = "DATAMART_CONNECTION_STRING",
        tables_config_path: str = "config/tables.yaml",
    ) -> None:
        load_dotenv("config/.env", override=False)
        self.datamart_env_key = datamart_env_key
        self.tables_config_path = Path(tables_config_path)
        self.tables_config = self._load_tables_config()
        self.facility_registry = self._build_facility_registry()

    def _load_tables_config(self) -> dict:
        if not self.tables_config_path.exists():
            raise FileNotFoundError(f"Không tìm thấy file cấu hình YAML: {self.tables_config_path}")
        with self.tables_config_path.open("r", encoding="utf-8") as stream:
            data = yaml.safe_load(stream) or {}
        return data

    def _build_facility_registry(self) -> dict[str, FacilityDefinition]:
        facilities_cfg = self.tables_config.get("facilities", {})
        registry: dict[str, FacilityDefinition] = {}

        for facility_code, cfg in facilities_cfg.items():
            normalized = str(facility_code).strip().lower()
            if not normalized:
                continue
            schema_name = str(cfg.get("staging_schema", "")).strip()
            if not schema_name:
                raise ValueError(f"Thiếu staging_schema cho facility '{normalized}' trong {self.tables_config_path}")

            registry[normalized] = FacilityDefinition(
                code=normalized,
                prod_env_key=f"PROD_CONNECTION_{normalized.upper()}",
                schema_name=schema_name,
            )

        if not registry:
            raise ValueError(f"Không có facility hợp lệ trong file {self.tables_config_path}")

        return registry

    def _get_facility_yaml_config(self, facility_code: str) -> dict:
        facilities_cfg = self.tables_config.get("facilities", {})
        facility_cfg = facilities_cfg.get(facility_code, {})
        if not facility_cfg:
            raise ValueError(f"Không tìm thấy cấu hình facility '{facility_code}' trong {self.tables_config_path}")
        return facility_cfg

    def _resolve_facility_keys_from_yaml(self, facility_code: str) -> tuple[int, int]:
        facility_cfg = self._get_facility_yaml_config(facility_code)
        try:
            nguon_key = int(facility_cfg.get("nguon_dulieu_key", -1))
            co_so_key = int(facility_cfg.get("co_so_key", -1))
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"nguon_dulieu_key/co_so_key của facility '{facility_code}' phải là số nguyên"
            ) from exc

        return nguon_key, co_so_key

    @staticmethod
    def _parse_facility_tokens(raw_value: str) -> list[str]:
        return [token.strip().lower() for token in raw_value.split(",") if token.strip()]

    def _resolve_target_facilities(self, target_facilities: list[str] | None = None) -> list[str]:
        if target_facilities is not None:
            normalized = [facility.strip().lower() for facility in target_facilities if facility.strip()]
            if not normalized or "all" in normalized:
                return list(self.facility_registry.keys())
            return normalized

        yaml_facilities = self.tables_config.get("etl_settings", {}).get("active_facilities", [])
        if not yaml_facilities:
            return list(self.facility_registry.keys())
        normalized = [str(facility).strip().lower() for facility in yaml_facilities if str(facility).strip()]
        return normalized or list(self.facility_registry.keys())

    def _validate_target_facilities(self, facilities: list[str]) -> None:
        unknown = [facility for facility in facilities if facility not in self.facility_registry]
        if unknown:
            valid = ", ".join(self.facility_registry.keys())
            raise ValueError(f"Facility không hợp lệ: {unknown}. Danh sách hợp lệ: {valid}")

    def _build_dimension_loader(
        self,
        datamart_connection: str,
        production_connection: str,
        facility: FacilityDefinition,
        nguon_dulieu_key: int,
        co_so_key: int,
    ) -> DimensionLoader:
        return DimensionLoader(
            datamart_connection=datamart_connection,
            production_connection=production_connection,
            facility_code=facility.code,
            facility_schema=facility.schema_name,
            nguon_dulieu_key=nguon_dulieu_key,
            co_so_key=co_so_key,
        )

    def _build_fact_loader(
        self,
        datamart_connection: str,
        production_connection: str,
        facility: FacilityDefinition,
        nguon_dulieu_key: int,
        co_so_key: int,
    ) -> FactLoader:
        return FactLoader(
            datamart_connection=datamart_connection,
            production_connection=production_connection,
            facility_code=facility.code,
            facility_schema=facility.schema_name,
            nguon_dulieu_key=nguon_dulieu_key,
            co_so_key=co_so_key,
        )

    def run(
        self,
        target_facilities: list[str] | None = None,
        run_dimension: bool = True,
        run_fact: bool = True,
        to_date: date | None = None,
    ) -> None:
        if not run_dimension and not run_fact:
            raise ValueError("Cần bật ít nhất một luồng: run_dimension hoặc run_fact")

        datamart_connection = os.getenv(self.datamart_env_key, "").strip()
        if not datamart_connection:
            raise ValueError(f"Thiếu biến môi trường {self.datamart_env_key}")

        selected_facilities = self._resolve_target_facilities(target_facilities)
        self._validate_target_facilities(selected_facilities)

        effective_to_date = to_date or date.today()
        print(f"[SyncOrchestrator] Danh sách facility cần chạy: {selected_facilities}")

        for facility_code in selected_facilities:
            facility = self.facility_registry[facility_code]
            production_connection = os.getenv(facility.prod_env_key, "").strip()
            if not production_connection:
                print(f"[SyncOrchestrator] Bỏ qua {facility.code} vì thiếu {facility.prod_env_key}")
                continue

            nguon_dulieu_key, co_so_key = self._resolve_facility_keys_from_yaml(facility.code)

            print(f"[SyncOrchestrator] Bắt đầu facility={facility.code}")
            try:
                if run_dimension:
                    dimension_loader = self._build_dimension_loader(
                        datamart_connection=datamart_connection,
                        production_connection=production_connection,
                        facility=facility,
                        nguon_dulieu_key=nguon_dulieu_key,
                        co_so_key=co_so_key,
                    )
                    dimension_loader.execute_load(to_date=effective_to_date)

                if run_fact:
                    fact_loader = self._build_fact_loader(
                        datamart_connection=datamart_connection,
                        production_connection=production_connection,
                        facility=facility,
                        nguon_dulieu_key=nguon_dulieu_key,
                        co_so_key=co_so_key,
                    )
                    fact_loader.execute_load(to_date=effective_to_date)

                print(f"[SyncOrchestrator] Hoàn tất facility={facility.code}")
            except Exception:
                print(f"[SyncOrchestrator] Lỗi tại facility={facility.code}, dừng luồng tuần tự")
                raise


def _parse_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chạy đồng bộ ETL tuần tự theo facility")
    parser.add_argument(
        "--facilities",
        type=str,
        default="ALL",
        help="Danh sách facility phân tách bởi dấu phẩy, ví dụ: hanoi,hcm hoặc ALL",
    )
    parser.add_argument(
        "--only",
        type=str,
        choices=["dimension", "fact", "all"],
        default="all",
        help="Giới hạn luồng chạy",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_cli_args()
    orchestrator = SyncOrchestrator()

    run_dimension = args.only in {"dimension", "all"}
    run_fact = args.only in {"fact", "all"}
    target_facilities = None if args.facilities.upper() == "ALL" else [token.strip() for token in args.facilities.split(",")]

    orchestrator.run(
        target_facilities=target_facilities,
        run_dimension=run_dimension,
        run_fact=run_fact,
    )
