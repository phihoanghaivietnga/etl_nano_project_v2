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