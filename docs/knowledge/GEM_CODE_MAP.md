# GEM_CODE_MAP.md

## Mục tiêu cập nhật
- Chuẩn hóa quy tắc ánh xạ tệp theo nhóm tri thức để phục vụ điều phối lâu dài.
- Làm cơ sở gộp file Master cho quy trình tạo tri thức đưa vào NotebookLM.

## Bảng quy tắc ánh xạ nhóm

### Nhóm CORE_LOGIC
- Phạm vi:
  - `/src/core/`
  - `/config/`
  - Tệp `.env` tại root
- File Master tương ứng: `MASTER_CORE_LOGIC.md`

### Nhóm ETL_PROCESS
- Phạm vi:
  - `/src/jobs/`
  - `/src/db/templates/sql/`
- File Master tương ứng: `MASTER_ETL_PROCESS.md`

### Nhóm INTERFACE
- Phạm vi:
  - `/src/ui/`
  - `/scripts/`
  - `main.py` tại root
- File Master tương ứng: `MASTER_INTERFACE.md`

#### Bổ sung theo yêu cầu 20260514_1420_tao_man_hinh_dashboard_doi_chieu_v1
- File UI mới:
  - `src/ui/dashboard_app.py`
- File lõi dùng chung phục vụ UI Manual Runner:
  - `src/core/base_ui.py`
  - `src/core/base_loader.py`
- SQL template đối chiếu dùng cho màn hình giao diện:
  - `src/db/templates/sql/dashboard_doichieu/ho_so_kham_benh_ngoai_tru_doi_chieu.sql`

#### Bổ sung theo yêu cầu 20260515_0835_tao_man_hinh_dashboard_doi_chieu_v2
- Entry UI mới theo mô hình phân trang:
  - `src/ui/main_app.py`
- Trang giao diện tách file độc lập:
  - `src/ui/pages/__init__.py`
  - `src/ui/pages/common.py`
  - `src/ui/pages/doi_chieu_page.py`
  - `src/ui/pages/manual_runner_page.py`
  - `src/ui/pages/job_history_page.py`
  - `src/ui/pages/bao_cao_page.py`
- Backend đối chiếu bất đồng bộ:
  - `src/ui/dashboard_app.py`
- Base class lõi dùng chung cho UI và Loader:
  - `src/core/base_ui.py`
  - `src/core/base_loader.py`
- SQL template đối chiếu theo domain:
  - `src/db/templates/sql/dashboard_doichieu/dim_luot_kham/production.sql`
  - `src/db/templates/sql/dashboard_doichieu/dim_luot_kham/staging.sql`
  - `src/db/templates/sql/dashboard_doichieu/dim_luot_kham/datamart.sql`
  - `src/db/templates/sql/dashboard_doichieu/fact_thu_phi_dich_vu/production.sql`
  - `src/db/templates/sql/dashboard_doichieu/fact_thu_phi_dich_vu/staging.sql`
  - `src/db/templates/sql/dashboard_doichieu/fact_thu_phi_dich_vu/datamart.sql`

### Nhóm KNOWLEDGE_BASE
- Phạm vi:
  - `/docs/knowledge/`
  - `agents.md`
  - `README.md`
  - `PROJECT_CHRONICLE.md`
- File Master tương ứng: `MASTER_KNOWLEDGE_BASE.md`

## Quy tắc phục vụ merge tri thức
- Mỗi nhóm được gộp thành một file Master riêng trong `temp_merged/`.
- Mỗi file Master phải có:
  - Mục lục liệt kê đầy đủ tệp nguồn.
  - Các khối nội dung phân tách bằng header `### SOURCE: <đường dẫn tệp>`.
  - Nội dung gốc được bọc trong code block Markdown theo đuôi tệp.
- Luồng gộp này là đầu vào chuẩn cho NotebookLM để đảm bảo giữ ngữ cảnh theo nhóm chức năng.