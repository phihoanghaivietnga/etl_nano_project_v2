from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from datetime import date

from dotenv import load_dotenv

from src.jobs.dimension_loader import DimensionLoader
from src.jobs.fact_loader import FactLoader


@dataclass(frozen=True)
class FacilityDefinition:
    code: str
    prod_env_key: str
    schema_name: str
    nguon_dulieu_env_key: str
    co_so_env_key: str
    default_nguon_dulieu_key: int
    default_co_so_key: int


class SyncOrchestrator:
    def __init__(
        self,
        datamart_env_key: str = "DATAMART_CONNECTION_STRING",
        active_facilities_env_key: str = "ACTIVE_FACILITIES",
    ) -> None:
        load_dotenv("config/.env", override=False)
        self.datamart_env_key = datamart_env_key
        self.active_facilities_env_key = active_facilities_env_key

        self.facility_registry: dict[str, FacilityDefinition] = {
            "hanoi": FacilityDefinition(
                code="hanoi",
                prod_env_key="PROD_CONNECTION_HANOI",
                schema_name="hanoi_hisnano_v2",
                nguon_dulieu_env_key="NGUON_DULIEU_KEY_HANOI",
                co_so_env_key="CO_SO_KEY_HANOI",
                default_nguon_dulieu_key=2,
                default_co_so_key=1,
            ),
            "hcm": FacilityDefinition(
                code="hcm",
                prod_env_key="PROD_CONNECTION_HCM",
                schema_name="hcm_hisnano_v2",
                nguon_dulieu_env_key="NGUON_DULIEU_KEY_HCM",
                co_so_env_key="CO_SO_KEY_HCM",
                default_nguon_dulieu_key=3,
                default_co_so_key=2,
            ),
            "halong": FacilityDefinition(
                code="halong",
                prod_env_key="PROD_CONNECTION_HALONG",
                schema_name="halong_hisnano_v2",
                nguon_dulieu_env_key="NGUON_DULIEU_KEY_HALONG",
                co_so_env_key="CO_SO_KEY_HALONG",
                default_nguon_dulieu_key=4,
                default_co_so_key=3,
            ),
            "haiphong": FacilityDefinition(
                code="haiphong",
                prod_env_key="PROD_CONNECTION_HAIPHONG",
                schema_name="haiphong_hisnano_v2",
                nguon_dulieu_env_key="NGUON_DULIEU_KEY_HAIPHONG",
                co_so_env_key="CO_SO_KEY_HAIPHONG",
                default_nguon_dulieu_key=5,
                default_co_so_key=4,
            ),
        }

    @staticmethod
    def _parse_facility_tokens(raw_value: str) -> list[str]:
        return [token.strip().lower() for token in raw_value.split(",") if token.strip()]

    def _resolve_target_facilities(self, target_facilities: list[str] | None = None) -> list[str]:
        if target_facilities is not None:
            normalized = [facility.strip().lower() for facility in target_facilities if facility.strip()]
            if not normalized or "all" in normalized:
                return list(self.facility_registry.keys())
            return normalized

        env_value = os.getenv(self.active_facilities_env_key, "ALL").strip()
        if not env_value or env_value.upper() == "ALL":
            return list(self.facility_registry.keys())
        return self._parse_facility_tokens(env_value)

    def _validate_target_facilities(self, facilities: list[str]) -> None:
        unknown = [facility for facility in facilities if facility not in self.facility_registry]
        if unknown:
            valid = ", ".join(self.facility_registry.keys())
            raise ValueError(f"Facility không hợp lệ: {unknown}. Danh sách hợp lệ: {valid}")

    def _resolve_facility_key(self, env_key: str, fallback: int) -> int:
        raw = os.getenv(env_key, "").strip()
        if not raw:
            return fallback
        try:
            return int(raw)
        except ValueError as exc:
            raise ValueError(f"Biến {env_key} phải là số nguyên, đang nhận '{raw}'") from exc

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

            nguon_dulieu_key = self._resolve_facility_key(
                facility.nguon_dulieu_env_key,
                facility.default_nguon_dulieu_key,
            )
            co_so_key = self._resolve_facility_key(
                facility.co_so_env_key,
                facility.default_co_so_key,
            )

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
