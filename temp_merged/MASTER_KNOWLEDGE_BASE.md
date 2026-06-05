# MASTER_KNOWLEDGE_BASE.md

## NHÓM: KNOWLEDGE_BASE

## MỤC LỤC NGUỒN
  [DESCRIPTION]: Project documentation and knowledge base

### PROJECT_CHRONICLE.md - Nhật ký thay đổi hạ tầng, sự cố và quyết định kỹ thuật theo mốc thời gian
### README.md - Tổng quan dự án, kiến trúc thư mục và hướng dẫn sử dụng nhanh
### agents.md - Định nghĩa cấu hình và chiến lược điều phối các AI Agent trong hệ thống
### docs/knowledge/GEM_AUTO_PIPELINE.md - Mô tả cơ chế vận hành pipeline tự động
### docs/knowledge/GEM_CODE_MAP.md - Bản đồ cấu trúc mã nguồn và quy tắc ánh xạ nhóm
### docs/knowledge/GEM_CODE_SNIPPETS.md - Thư viện mẫu code chuẩn dùng trong các tình huống phổ biến
### docs/knowledge/GEM_DATA_FLOW.md - Mô tả luồng dữ liệu từ Production qua Staging tới Datamart
### docs/knowledge/GEM_DB_SCHEMAS.md - Đặc tả schema và cấu trúc bảng dữ liệu
### docs/knowledge/GEM_DEPENDENCY_GRAPH.md - Đồ thị phụ thuộc giữa module, lớp và quy trình
### docs/knowledge/GEM_ERROR_CONTEXT.md - Ngữ cảnh lỗi chuẩn hóa và hướng xử lý theo mã lỗi
### docs/knowledge/GEM_GUIDE.md - Thứ tự ưu tiên đọc tài liệu cho từng loại tác vụ
### docs/knowledge/GEM_NAVIGATION.md - Chỉ dẫn điều hướng và tra cứu nhanh các tài liệu tri thức
### docs/knowledge/GEM_SYNC_WORKFLOW.md - Quy trình đồng bộ sai khác và cơ chế Enhanced Merge
### docs/knowledge/GEM_TECHNICAL_STANDARDS.md - Tiêu chuẩn kỹ thuật, bảo mật và xác thực tích hợp
### docs/knowledge/loop_Gem_Github_GoogleDrive_NotebookLM.md - Vòng lặp cộng tác tri thức giữa Gemini, GitHub, Drive và NotebookLM

## NỘI DUNG GỘP

### SOURCE: PROJECT_CHRONICLE.md
```md
# PROJECT_CHRONICLE.md

## 2026-06-02

### ADR-37: Cập nhật Schema Datamart & Logic Phân loại Khách hàng

**Ngày thực hiện:** 2026-06-02

**Master:** Đã chủ động nâng cấp hạ tầng Datamart và cập nhật logic nghiệp vụ.

**Chi tiết thay đổi:**

1. **Schema Datamart mở rộng:**
   - Bổ sung trường `MaGoiDichVu` (VARCHAR(50)) vào bảng `dm.FactThuPhiDichVu`
   - Trường này phục vụ logic gom nhóm bằng Window Function phục vụ đo lường chỉ số Khách hàng Trung thành

2. **Logic nghiệp vụ phân loại Khách hàng mới:**
   - **Khách quay lại (Cross-sell):** Lần đến viện >= 2 và có phát sinh ít nhất 01 Dịch Vụ mới hoàn toàn
   - **Khách tái khám (Retention):** Dịch vụ phát sinh thuộc nhóm "Khám bệnh" và chứa từ khóa '%tái khám%'
   - **Khách trung thành (Loyalty):** Window Function theo MaBenhNhan và MaGoiDichVu, số lượng dịch vụ >= 2

3. **SQL Template cập nhật:**
   - File `src/db/templates/sql/fact/merge_fact_thuphichvu_3in1.sql` đã được chỉnh sửa để đồng bộ trường `MaGoiDichVu` từ Tầng 2 lên Tầng 3

4. **Khung Python Core:**
   - Không có sự thay đổi nào trong mã nguồn Python
   - Luồng Incremental V2 đã hỗ trợ đồng bộ metadata động nên không cần cập nhật code

**Tác động:**
- Hỗ trợ đo lường và phân tích hành vi khách hàng theo các gói dịch vụ
- Phục vụ báo cáo phân khúc khách hàng và các chiến lược giữ chân

**Tài liệu đã cập nhật:**
- `docs/knowledge/GEM_DB_SCHEMAS.md` - Schema bảng dm.FactThuPhiDichVu với trường MaGoiDichVu
- `docs/knowledge/GEM_DATA_FLOW.md` - Quy tắc phân loại Khách hàng (Quay lại, Tái khám, Trung thành)

---

## 2026-05-09

### Dấu mốc: Xây dựng hệ thống gộp tri thức đa tầng cho NotebookLM
- Thiết lập quy tắc ánh xạ tệp theo 4 nhóm chuẩn: `CORE_LOGIC`, `ETL_PROCESS`, `INTERFACE`, `KNOWLEDGE_BASE`.
- Nâng cấp script `scripts/upload_to_drive_from_local.py` để:
  - Lọc tệp theo `.gitignore` và blacklist cứng.
  - Gộp nội dung theo nhóm vào các file Master trong `temp_merged/`.
  - Bảo tồn ngữ cảnh bằng mục lục nguồn và header `### SOURCE: <đường dẫn tệp>`.
  - Đối soát MD5 trước khi create/update trên Google Drive.
  - Đồng bộ mọi file `.md` dưới dạng Google Docs.
- Cập nhật tài liệu tri thức vận hành để phản ánh luồng mới:
  - Quét file -> Lọc tệp -> Ánh xạ nhóm -> Gộp nội dung -> Đối soát MD5 -> Upload.

### Ý nghĩa kỹ thuật
- Chuẩn hóa đầu vào tri thức cho NotebookLM theo ngữ cảnh chức năng.
- Giảm thời gian đồng bộ nhờ chỉ upload phần sai khác.
- Nâng tính truy vết và khả năng bảo trì tài liệu kỹ thuật theo thời gian.

## 2026-05-11

### Sự cố: Thư mục `tmp_diffsync_demo` đặt sai vị trí trong `docs/knowledge/`
- **Vấn đề**: Thư mục demo `tmp_diffsync_demo/` nằm trong `docs/knowledge/`, gây nhiễu cho bộ não AI (NotebookLM) khi quét tri thức.
- **Nguyên nhân**: Trong lần triển khai trước, thư mục demo được tạo trực tiếp trong `docs/knowledge/` thay vì thư mục gốc project.
- **Cách khắc phục**:
  1. Di chuyển `docs/knowledge/tmp_diffsync_demo/` ra thư mục gốc project (`/tmp_diffsync_demo/`).
  2. Cập nhật `GEM_CODE_MAP.md`: Thay `/docs/v2_knowledge/` bằng `/docs/knowledge/` cho đúng cấu trúc thực tế.
  3. Cập nhật `config/.env`: Đổi `GDRIVE_ROOT_DIR=etl_nano_project_v2` thành `GDRIVE_ROOT_DIR=docs/knowledge` để script quét đúng phạm vi.
  4. Nâng cấp script `upload_to_drive_from_local.py`:
     - Sửa hàm `classify_group_by_path` để xử lý đúng khi `GDRIVE_ROOT_DIR` trỏ đến thư mục con.
     - Thêm `[DESCRIPTION]` metadata vào mục lục mỗi file Master.
     - Bổ sung log chi tiết: lọc file, đối soát MD5, upload/create/update.
- **Bài học kinh nghiệm**:
  - Không bao giờ đặt thư mục demo hay tệp tạm trong `docs/knowledge/` vì đây là nguồn dữ liệu tri thức cho NotebookLM.
  - Mọi thay đổi cấu trúc thư mục cần được ghi nhận ngay vào `PROJECT_CHRONICLE.md` để tránh mất dấu.
  - Script cần có khả năng xử lý cả hai chế độ: root = project root hoặc root = thư mục con (subdirectory).

### Sự cố khẩn cấp: Thu hẹp sai phạm vi quét về `docs/knowledge`
- **Vấn đề**: `GDRIVE_ROOT_DIR` đã bị thu hẹp về `docs/knowledge`, làm mất khả năng quét toàn bộ layer từ gốc dự án.
- **Tác động**:
  - Hàm phân loại theo path không phản ánh đúng kiến trúc tổng thể.
  - Các nhóm Master ngoài `KNOWLEDGE_BASE` có nguy cơ thiếu dữ liệu.
- **Khắc phục đã thực hiện**:
  1. Khôi phục `GDRIVE_ROOT_DIR=etl_nano_project_v2` trong `config/.env`.
  2. Viết lại `classify_group_by_path` theo path vật lý từ root project:
     - `/src/core/` hoặc `/config/` hoặc `.env` -> `CORE_LOGIC`
     - `/src/jobs/` hoặc `/src/db/templates/sql/` -> `ETL_PROCESS`
     - `/src/ui/` hoặc `/scripts/` hoặc `main.py` -> `INTERFACE`
     - `/docs/knowledge/` hoặc file chiến lược root -> `KNOWLEDGE_BASE`
  3. Chuẩn hóa mục lục Master theo dạng `### [PATH] - [DESCRIPTION]`.
  4. Chạy lại đồng bộ toàn dự án để xác thực log và số lượng file theo nhóm.
- **Kết quả**:
  - Script quét từ root project thành công (`ROOT_DIR=.../etl_nano_project_v2`).
  - Group `KNOWLEDGE_BASE` có dữ liệu rõ ràng; mục lục Master đã hiển thị theo format mới.
  - Group `CORE_LOGIC` trong lần chạy hiện tại chưa có nguồn hợp lệ sau lọc vì `src/core` rỗng và các file nhạy cảm trong `config/` bị loại theo chính sách `.gitignore`/forced-exclude.

### Hoàn tất giai đoạn hạ tầng đồng bộ đa nền tảng
- **Mốc thời gian**: 2026-05-11
- **Trạng thái**: Hoàn thành giai đoạn Infrastructure Phase cho luồng tri thức Gemini - Codex - GitHub - Drive - NotebookLM.
- **Giải trình số lượng file bị loại lớn (>2200 file)**:
  - Phần lớn file bị loại nằm trong thư mục môi trường ảo `.venv` và thư mục hệ thống `.git`.
  - Đây là hành vi đúng theo quy tắc lọc `pathspec` + forced exclude để tránh đồng bộ file không phục vụ tri thức nghiệp vụ.
- **Xác nhận cấu trúc `/src/` đang trống**:
  - `src/core/` và `src/jobs/` trống là đúng chủ đích hiện tại.
  - Dự án đang ưu tiên xây dựng pipeline trao đổi tri thức và cơ chế đồng bộ trước khi nạp code nghiệp vụ ETL chi tiết.
```

### SOURCE: README.md
```md
# ETL NANO PROJECT V2

## 1. Mục đích hệ thống
Hệ thống ETL phiên bản v2 được thiết kế để chuẩn hóa luồng dữ liệu từ Production sang Datamart theo kiến trúc Modular và lập trình hướng đối tượng (OOP). Hệ thống đảm bảo tính thống nhất giữa chế độ chạy Tự động (Auto) và Thủ công (Manual).
Hy vọng test lần cuối
Lần cuối 2
Lần cuối 3

## 2. Cấu trúc thư mục
ETL_Nano_Project_V2/
├── agents.md               # File chiến lược điều phối hệ thống
├── README.md               # Hướng dẫn tổng quan dự án
├── .env                    # Lưu trữ biến môi trường và kết nối DB
├── config/                 # Cấu hình hệ thống và danh sách bảng
├── docs/
│   ├── knowledge/       # Tầng tri thức GEM
		├── GEM_NAVIGATION.md: Chỉ dẫn tìm kiếm tri thức.
		├── GEM_GUIDE.md: Thứ tự ưu tiên đọc tài liệu.
		├── GEM_CODE_MAP.md: Sơ đồ các lớp và hàm trong mã nguồn.
		├── GEM_CODE_SNIPPETS.md: Thư viện mã mẫu chuẩn.
		├── GEM_DATA_FLOW.md: Mô tả luồng dữ liệu Production -> Staging -> Datamart.
		├── GEM_DB_SCHEMAS.md: Chi tiết cấu trúc bảng và schema database.
		├── GEM_AUTO_PIPELINE.md: Chi tiết vận hành engine chạy tự động.
		├── GEM_DEPENDENCY_GRAPH.md: Đồ thị mối quan hệ giữa các module.
		├── GEM_ERROR_CONTEXT.md: Bối cảnh và cách xử lý các mã lỗi (E-ID).
		├── GEM_TECHNICAL_STANDARDS.md: Tiêu chuẩn kỹ thuật và xác thực Google Drive.
		├── GEM_SYNC_WORKFLOW.md: Quy trình đồng bộ sai khác (Diff Sync) giữa local và Google Drive.
│   └── archive/            # Lưu trữ tài liệu phiên bản cũ
├── scripts/                # CÁC SCRIPT VẬN HÀNH VÀ TỰ ĐỘNG HÓA
│   └── upload_to_drive.py  # Script đồng bộ tri thức lên Google Drive
├── src/                    # Mã nguồn chính của ứng dụng, phân tách giữa Core logic và Job thực thi.
│   ├── core/               # Lớp cha, Logger, Database Connection
│   ├── jobs/               # Logic đồng bộ các bảng cụ thể
│   ├── ui/                 # Giao diện Streamlit (Runner & Verify)
│   └── db/
│       └── templates/sql/  # Nguồn SQL MERGE duy nhất
├── tests/                  # Script kiểm thử độc lập
└── .github/
    └── workflows/
        └── sync_to_drive.yml # File cấu hình Trigger GitHub Actions

## 3. Ý nghĩa các file GEM tri thức (docs/knowledge/)
- GEM_NAVIGATION.md: Chỉ dẫn tìm kiếm tri thức.
- GEM_GUIDE.md: Thứ tự ưu tiên đọc tài liệu.
- GEM_CODE_MAP.md: Sơ đồ các lớp và hàm trong mã nguồn.
- GEM_CODE_SNIPPETS.md: Thư viện mã mẫu chuẩn.
- GEM_DATA_FLOW.md: Mô tả luồng dữ liệu Production -> Staging -> Datamart.
- GEM_DB_SCHEMAS.md: Chi tiết cấu trúc bảng và schema database.
- GEM_AUTO_PIPELINE.md: Chi tiết vận hành engine chạy tự động.
- GEM_DEPENDENCY_GRAPH.md: Đồ thị mối quan hệ giữa các module.
- GEM_ERROR_CONTEXT.md: Bối cảnh và cách xử lý các mã lỗi (E-ID).
- GEM_TECHNICAL_STANDARDS.md: Tiêu chuẩn kỹ thuật và xác thực Google Drive.
- GEM_SYNC_WORKFLOW.md: Quy trình đồng bộ sai khác (Diff Sync) giữa local và Google Drive.
```

### SOURCE: agents.md
```md
# CHIẾN LƯỢC ĐIỀU PHỐI HỆ THỐNG AGENTS

## 1. Vai trò
- Gem (Kiến trúc sư): Điều phối, ra lệnh và giám sát dựa trên Tầng tri thức.
- Codex (Thợ code): Thực thi lập trình, sửa lỗi và cập nhật tài liệu.

## 2. Giao thức làm việc
- Bước 1: Trước khi sửa code, Codex bắt buộc phải đọc các tệp GEM_xxx.md liên quan để nắm ngữ cảnh.
- Bước 2: Thực hiện sửa đổi mã nguồn.
- Bước 3: Cập nhật đúng và đủ các thay đổi vào Tầng tri thức (GEM_xxx.md) để đảm bảo tính nhất quán.
- Bước 4: Kết xuất báo cáo vào tệp REPORT_CHANGES.md tại thư mục gốc.

## 3. Quy tắc bắt buộc
- Ngôn ngữ: Tiếng Việt rõ ràng, ngắn gọn, cô đọng.
- Hình thức: Không sử dụng icon trong mọi tệp tài liệu .md.
- Kỹ thuật: Mọi mã nguồn phải theo hướng đối tượng (OOP), kế thừa từ Base Class tại src/core.

## 3.1. Điều luật kết nối cơ sở dữ liệu
- KẾT NỐI STAGING & DATAMART: Được phép thực thi các câu lệnh thay đổi dữ liệu và cấu trúc (TRUNCATE, INSERT, UPDATE, DELETE, MERGE, ALTER, CREATE).
- KẾT NỐI PRODUCTION: TUYỆT ĐỐI CẤM mọi câu lệnh làm thay đổi dữ liệu (CREATE, UPDATE, DELETE, TRUNCATE, ALTER, DROP, INSERT). Kết nối đến Production CHỈ ĐƯỢC PHÉP sử dụng để ĐỌC (SELECT) hoặc dùng cho công cụ trích xuất (BCP OUT).

## 4. Cấu trúc thư mục
ETL_Nano_Project_V2/
├── agents.md               # File chiến lược điều phối hệ thống
├── README.md               # Hướng dẫn tổng quan dự án
├── PROJECT_CHRONICLE.md    # Nhật ký tiến hóa của dự án
├── .env                    # Lưu trữ biến môi trường và kết nối DB
├── config/                 # Cấu hình hệ thống và danh sách bảng
├── docs/
│   ├── knowledge/       # Tầng tri thức GEM
		├── GEM_NAVIGATION.md: Chỉ dẫn tìm kiếm tri thức.
		├── GEM_GUIDE.md: Thứ tự ưu tiên đọc tài liệu.
		├── GEM_CODE_MAP.md: Sơ đồ các lớp và hàm trong mã nguồn.
		├── GEM_CODE_SNIPPETS.md: Thư viện mã mẫu chuẩn.
		├── GEM_DATA_FLOW.md: Mô tả luồng dữ liệu Production -> Staging -> Datamart.
		├── GEM_DB_SCHEMAS.md: Chi tiết cấu trúc bảng và schema database.
		├── GEM_AUTO_PIPELINE.md: Chi tiết vận hành engine chạy tự động.
		├── GEM_DEPENDENCY_GRAPH.md: Đồ thị mối quan hệ giữa các module.
		├── GEM_ERROR_CONTEXT.md: Bối cảnh và cách xử lý các mã lỗi (E-ID).
		├── GEM_TECHNICAL_STANDARDS.md: Tiêu chuẩn kỹ thuật và xác thực Google Drive.
		├── GEM_SYNC_WORKFLOW.md: Quy trình đồng bộ sai khác (Diff Sync) giữa local và Google Drive.
│   └── archive/            # Lưu trữ tài liệu phiên bản cũ
├── scripts/                # CÁC SCRIPT VẬN HÀNH VÀ TỰ ĐỘNG HÓA
│   └── upload_to_drive.py  # Script đồng bộ tri thức lên Google Drive
├── src/                    # Mã nguồn chính của ứng dụng
│   ├── core/               # Lớp cha, Logger, Database Connection
│   ├── jobs/               # Logic đồng bộ các bảng cụ thể
│   ├── ui/                 # Giao diện Streamlit (Runner & Verify)
│   └── db/
│       └── templates/sql/  # Nguồn SQL MERGE duy nhất
├── tests/                  # Script kiểm thử độc lập
└── .github/
    └── workflows/
        └── sync_to_drive.yml # File cấu hình Trigger GitHub Actions
```

### SOURCE: docs/knowledge/GEM_AUTO_PIPELINE.md
```md
# GEM_AUTO_PIPELINE.md

## Mục tiêu
- Chuẩn hóa engine tự động chạy ETL theo chiến lược tuần tự an toàn Landing.
- Hỗ trợ vận hành chọn lọc cơ sở để phục vụ deploy theo pha.

## Module điều phối
- Tệp: `src/jobs/sync_orchestrator.py`
- Lớp: `SyncOrchestrator`

## Quy tắc điều phối bắt buộc
1. Chạy tuần tự từng cơ sở, không chạy song song giữa các cơ sở.
2. Cơ sở hiện tại phải hoàn tất toàn bộ Dimension + Fact + cleanup Landing trước khi sang cơ sở kế tiếp.
3. Nếu có lỗi tại một cơ sở thì dừng luồng tuần tự để tránh lan lỗi.

## Selective Sync
- Hỗ trợ 2 cách chọn cơ sở chạy:
  - Cấu hình YAML: `config/tables.yaml` -> `etl_settings.active_facilities`
  - Tham số hàm: `run(target_facilities=['hanoi'])`
- Nếu không truyền hoặc nhận `ALL` thì chạy toàn bộ facility đã định nghĩa.
- Facility ngoài scope không được khởi tạo connection.

## Cấu hình vận hành tập trung (YAML)
- File chuẩn: `config/tables.yaml`
- Khối `etl_settings`:
  - `odbc_chunk_size`: kích thước lô nạp ODBC cho DimensionLoader.
  - `active_facilities`: danh sách cơ sở mặc định cho orchestrator.
- Khối `facilities.<facility_code>`:
  - `nguon_dulieu_key`, `co_so_key`, `staging_schema`.
- Quy tắc: ưu tiên YAML làm nguồn cấu hình chính cho matrix multi-tenant; `.env` chỉ giữ chuỗi kết nối.

## Input connection chuẩn
- Datamart: `DATAMART_CONNECTION_STRING`
- Production theo cơ sở:
  - `PROD_CONNECTION_HANOI`
  - `PROD_CONNECTION_HCM`
  - `PROD_CONNECTION_HALONG`
  - `PROD_CONNECTION_HAIPHONG`

## Luồng gọi loader
- Dimension: `src/jobs/dimension_loader.py`
- Fact: `src/jobs/fact_loader.py`
- Trình tự gọi trong mỗi facility:
  1. `DimensionLoader.execute_load(...)`
  2. `FactLoader.execute_load(...)`

## Chốt chặn vận hành
- FactLoader luôn dọn Landing ở đầu và cuối luồng.
- Hard delete incremental chỉ được áp dụng trong cửa sổ D-3 và đúng phạm vi cơ sở.
- MERGE Fact lên Datamart bắt buộc cô lập theo `NguonDuLieuKey`.

## Quy tắc chốt sổ cuối ngày (T-1)
- Auto Pipeline chi dung chien luoc End-of-Day Batching (chot so cuoi ngay).
- Bien `to_date` tai `SyncOrchestrator.run()` mac dinh = `date.today() - timedelta(days=1)` (ngay hom qua).
- Bien `from_date` duoc tinh tu `to_date` tru di `lookback_days` tu YAML.
- Tuyet doi khong lay du lieu cua ngay hien tai (T+0).
- Che do nay CHI ap dung cho Auto Pipeline; Manual Pipeline van nhan input ngay tu UI nguoi dung.

## Cơ chế Giám sát (Monitoring)
- Áp dụng tại `DimensionLoader`:
  - Log runtime dùng timestamp đến mili-giây theo format `YYYY-MM-DD HH:MM:SS.mmm` và `flush=True`.
  - Luồng ODBC copy log tiến độ theo tổng số dòng đã nạp từng lô.
  - Trạng thái MERGE ODS -> Datamart có log rõ ràng theo cặp:
    - `[START] Đang thực thi MERGE ODS -> Datamart cho <dimension_name>...`
    - `[SUCCESS] Hoàn thành MERGE <dimension_name>`
```

### SOURCE: docs/knowledge/GEM_CODE_MAP.md
```md
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

#### Bổ sung theo yêu cầu 20260518_0900_xay_dung_khung_dong_bo_v1
- Module điều phối ETL tuần tự có hỗ trợ Selective Sync:
  - `src/jobs/sync_orchestrator.py`
  - Chức năng chính:
    - Class `SyncOrchestrator` điều phối tuần tự theo facility.
    - Hỗ trợ lọc cơ sở chạy bằng `etl_settings.active_facilities` trong `config/tables.yaml` hoặc tham số `run(target_facilities=...)`.
    - Chỉ map/khởi tạo connection theo facility được chọn, bỏ qua facility ngoài scope.
- Module nạp Dimension full load 2-Hop:
  - `src/jobs/dimension_loader.py`
  - Chức năng chính:
    - Class `DimensionLoader` kế thừa `BaseLoader`.
    - Luồng Production -> ODS cơ sở bằng ODBC Bulk Copy native (`pyodbc.executemany`).
    - Luồng ODS cơ sở -> Datamart bằng MERGE SQL template có sẵn.
    - Logging real-time cho full-load:
      - Hàm `_log(self, message: str, **kwargs)` in timestamp đến mili-giây và `flush=True`.
      - `**kwargs` được dùng để tương thích đa hình với `BaseLoader._log(..., queue=..., loop=...)` trong luồng orchestrator.
      - Hàm `_copy_prod_to_ods(...)` đọc `odbc_chunk_size` từ `config/tables.yaml`.
      - Hàm `_copy_prod_to_ods(...)` đọc cấu hình facility từ YAML để lấy `nguon_dulieu_key` và `co_so_key` theo `facility_code`.
      - Hàm `_copy_prod_to_ods(...)` tự động Tenant Injection bằng cách nối thêm 3 cột `NguonDuLieuKey`, `CoSoKey`, `MaCoSo` vào payload insert ODS.
      - Chunking theo tham số YAML + commit theo lô để cân bằng hiệu năng và an toàn bộ nhớ.
      - Guard an toàn Production giữ nguyên: connection Production chỉ dùng truy vấn `SELECT`.
      - Trạng thái MERGE có cặp log `[START]` và `[SUCCESS]` trong `_execute_dimension_spec`.

#### Bổ sung theo yêu cầu 20260518_1040_xay_dung_luong_full_load_v1
- Chuẩn hóa phạm vi FULL_LOAD trong `DimensionLoader` chỉ còn đúng 4 dimension:
  - `DimBenhNhan`: `DMBenhNhan` -> `DimBenhNhan_merge.sql`
  - `DimBenh`: `DMBenh` -> `DimBenh_merge.sql`
  - `DimLoaiGoiDichVu`: `LoaiGoiDichVuNT` -> `DimLoaiGoiDichVu_merge.sql`
  - `DimDichVu`: (`DMLoaiDichVu`, `DMDichVu`, `DMDichVuChiTiet`) -> `dim_dich_vu_merge.sql`
- Quy tắc đặc biệt DimDichVu:
  - Bắt buộc chạy BCP đủ 3 bảng vào ODS trước khi gọi MERGE Datamart.
- Nợ kỹ thuật đã xử lý:
  - Gỡ `DimLuotKham` khỏi `DimensionLoader` để tránh `TRUNCATE` nhầm lên bảng có bản chất incremental.
  - Trạng thái theo dõi ở luồng Fact: `FactLoader.PENDING_INCREMENTAL_DIMENSIONS = ("DimLuotKham",)`.
- Quân luật an toàn DB trong `DimensionLoader`:
  - `production_connection` chỉ dùng cho `SELECT`/`BCP OUT`.
  - `TRUNCATE` và `MERGE` chỉ thực thi bằng connection Datamart/ODS.
- Module nạp Fact incremental 3-Hop:
  - `src/jobs/fact_loader.py`
  - Chức năng chính:
    - Class `FactLoader` kế thừa `BaseLoader`.
    - Luồng Prod -> Landing `stg_nano_v2` theo cửa sổ trượt D-3.
    - Luồng Landing -> ODS bằng MERGE có hard delete giới hạn D-3.
    - Luồng ODS -> Datamart bằng MERGE batching `TOP (10000)`.
    - Áp dụng fallback seed key `-1` cho early arriving facts.
    - Dọn Landing ở đầu và cuối luồng để chống rò rỉ dữ liệu giữa facilities.

#### Bổ sung theo yêu cầu 20260519_1315_sync_incremental_v1
- Cấu phần lõi mới cho incremental động:
  - `src/core/base_extractor.py`
  - Chức năng chính:
    - `ExtractPlan`: DTO mô tả kế hoạch extract (`table_name`, `date_column`, `effective_from_date`, `to_date`, `select_sql`, `selected_columns`, `projected_columns`).
    - `DynamicColumnProjection`: DTO cột động gồm `column_name`, `data_type`, `select_expression`, `is_masked`.
    - `BaseExtractor.normalize_date(...)`: chuẩn hóa input ngày (`date`, `datetime`, `YYYY-MM-DD`).
    - `BaseExtractor.compute_effective_from_date(...)`: áp dụng lookback động `from_date - lookback_days`.
    - `BaseExtractor.build_dynamic_select_columns(...)`: đọc metadata từ `INFORMATION_SCHEMA.COLUMNS`, giữ đủ thứ tự cột theo `ORDINAL_POSITION` và mask cột thuộc `exclude_datatypes` bằng `CAST(NULL AS VARCHAR(1)) AS [TenCot]`.
    - `BaseExtractor.build_select_sql(...)`: sinh Dynamic SELECT theo projection expressions đã mask để chống lệch schema BCP (`22005`).
- Tái cấu trúc `src/jobs/fact_loader.py` theo ma trận YAML:
  - Đọc node `incremental_tables` từ `config/tables.yaml` thành `FactTableSpec`.
  - Bỏ hardcode danh sách bảng fact, chuyển sang cấu hình động theo từng bảng.
  - Bổ sung guard `validate_sql_revenue_rules(...)` (Regex) để bảo vệ logic fallback doanh thu `COALESCE/ISNULL` trên các template doanh thu.
  - Luồng 3 tầng chuẩn hóa:
    1. Tầng 1: `TRUNCATE` global landing `stg_nano_v2` + BCP `-w`.
    2. Tầng 2: MERGE từ landing sang facility staging, không dùng `TRUNCATE`.
    3. Tầng 3: thực thi SQL template có sẵn qua `merge_script`, không sửa file SQL template.
  - Bổ sung chốt chống treo lock:
    - Sau `TRUNCATE` landing có `connection.commit()` ngay để tránh lock chờ giữa `pyodbc` session và tiến trình BCP IN.
  - Bổ sung chốt sanitize logging:
    - `src/core/base_loader.py` ẩn nội dung query/command khi log BCP UTF-16-LE để tránh rò rỉ thông tin nhạy cảm.
- Cập nhật điều phối:
  - `src/jobs/sync_orchestrator.py` truyền `tables_config_path` vào `FactLoader` để đồng bộ cùng một nguồn cấu hình YAML.
- Mở rộng cấu hình:
  - `config/tables.yaml` có node `incremental_tables` cho các bảng:
    - `ThuPhiDichVu`, `ThuPhiBaoHiem`, `ThuPhiTangGiam` (date: `NgayDenKham`)
    - `ThuPhiGoi` (date: `NgayThu`)
    - `DoThiLuc` (date: `NgayDo`)
    - `HoSoKhamBenhNgoaiTru` (date: `NgayVaoKham`, type `fact`, merge `DimLuotKham_merge.sql`)

#### Bổ sung theo yêu cầu 20260520_1110_sync_incremental_v4
- Chuẩn hóa xử lý metadata cột ở `src/core/base_extractor.py`:
  - Trong `BaseExtractor.build_dynamic_select_columns(...)`, bắt buộc `.strip()` ngay tại điểm đọc metadata từ `pyodbc`:
    - `column_name = str(row[0]).strip()`
    - `data_type = str(row[1]).strip().lower()`
- Bổ sung năng lực BCP chuẩn ở `src/core/base_loader.py`:
  - `BaseLoader.parse_connection_string(...)` dùng Regex `re.IGNORECASE` để bóc tách connection string.
  - `BaseLoader._build_bcp_connection_args(...)` map tham số kết nối cho BCP: `-S`, `-d`, và auth `-U/-P` hoặc `-T`.
  - `BaseLoader.run_bcp_utf16le(...)` nhận thêm `source_connection_string` để bắt buộc BCP OUT dùng kết nối nguồn Production.
  - `BaseLoader.run_bcp_in(...)` mới cho BCP IN, bắt buộc đủ cờ: `-w`, `-k`, `-E`, `-t\t`, `-r\n`.
  - `BaseLoader._mask_bcp_command(...)` dùng để log command BCP IN có che mật khẩu.
- Chuẩn hóa transaction biên trong `src/jobs/fact_loader.py`:
  - Tầng 1 chạy theo thứ tự cứng:
    1. BCP OUT từ Production.
    2. Mở connection A -> `TRUNCATE` Landing -> `commit()` -> đóng connection A.
    3. BCP IN vào Landing bằng session subprocess riêng.
    4. Mở connection B mới để chạy các bước MERGE tầng sau.

#### Bổ sung theo yêu cầu 20260520_1435_sync_incremental_v5
- Chuyển kiến trúc incremental từ Black-list sang Whitelist cột:
  - `config/tables.yaml`:
    - Xóa toàn bộ `exclude_datatypes`.
    - Mỗi bảng incremental bắt buộc khai báo `selected_columns`.
- Vai trò mới của `src/core/base_extractor.py`:
  - Không còn quét `INFORMATION_SCHEMA.COLUMNS`.
  - Không còn `DynamicColumnProjection` và logic masking datatype.
  - Sinh Dynamic SELECT trực tiếp từ `selected_columns`.
  - Tự ghép 3 cột enrichment vào projection:
    - `{co_so_key} AS [CoSoKey]`
    - `{nguon_du_lieu_key} AS [NguonDuLieuKey]`
    - `'{ma_co_so}' AS [MaCoSo]`
- Vai trò mới của `src/jobs/fact_loader.py`:
  - `FactTableSpec` đổi sang giữ `selected_columns`.
  - `build_extract_plan(...)` nhận trực tiếp `selected_columns` + 3 biến ngữ cảnh (`co_so_key`, `nguon_du_lieu_key`, `ma_co_so`).
  - Luồng Tầng 1 giữ biên giao dịch cô lập chống deadlock:
    1. BCP OUT hoàn tất.
    2. Connection A: `TRUNCATE` + `commit()` + đóng ngay.
    3. BCP IN bằng subprocess session riêng.
    4. Connection B mới để chạy MERGE tầng sau.

#### Bổ sung theo yêu cầu 20260520_1540_sync_incremental_v6
- Quyết định chiến lược mới cho Incremental:
  - Hủy hoàn toàn BCP trong luồng incremental.
  - Quay về pipeline PyODBC để ổn định ép kiểu ngầm (implicit casting).
- `src/core/base_extractor.py`:
  - `build_extract_plan(...)` chỉ còn nhận `selected_columns`.
  - Dynamic SELECT chỉ gồm các cột Whitelist, không ghép enrichment projection vào câu SELECT.
- `src/core/base_loader.py`:
  - Loại bỏ các hàm và tiện ích BCP:
    - `parse_connection_string(...)`
    - `_build_bcp_connection_args(...)`
    - `_mask_bcp_command(...)`
    - `run_bcp_utf16le(...)`
    - `run_bcp_in(...)`
- `src/jobs/fact_loader.py`:
  - Tầng 1 chuyển sang nạp PyODBC theo chunk:
    1. `cursor.execute(select_sql)` trên connection Production.
    2. `TRUNCATE stg_nano_v2.[TenBang]` đúng 1 lần trước vòng lặp.
    3. Dùng `fetchmany(batch_size)` + `executemany(...)` để nạp dữ liệu.
    4. `commit()` sau khi nạp xong Tầng 1.
  - Bắt buộc INSERT động tường minh:
    - `INSERT INTO [stg_nano_v2].[TenBang] ([Col1], [Col2], ...) VALUES (?, ?, ...)`.
  - Vẫn giữ kiến trúc Staging 3 tầng:
    - Tầng 1: Landing transient.
    - Tầng 2: MERGE landing -> facility staging.
    - Tầng 3: MERGE facility staging -> datamart.
- Script vận hành mới:
  - `scripts/sync_selected_columns_from_staging.py`:
    - Kết nối bằng `STAGING_CONNECTION_STRING`.
    - Quét `INFORMATION_SCHEMA.COLUMNS` theo `ORDINAL_POSITION` cho 6 bảng incremental.
    - `.strip()` tên cột, loại `MaCoSo/CoSoKey/NguonDuLieuKey`.
    - In preview YAML hoặc ghi trực tiếp `selected_columns` vào `config/tables.yaml` (`--write`).

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

#### Bổ sung theo yêu cầu 20260521_1055_fix_manual_pipeline_v1
- Điều phối Manual Runner đã chuyển từ `GenericTableLoader` sang Loader nghiệp vụ động theo bảng chọn:
  - `src/ui/pages/manual_runner_page.py`
  - Cấu hình nguồn chọn bảng đọc từ `config/tables.yaml`:
    - `incremental_tables` -> chạy `FactLoader` theo bảng đích + khoảng ngày nghiệp vụ.
    - danh mục full-load (`DimensionLoader.DEFAULT_DIMENSION_SPECS`) -> chạy `DimensionLoader` theo dimension đích.
- Mở rộng loader để cô lập chạy đơn đối tượng từ UI:
  - `src/jobs/fact_loader.py`:
    - `__init__(..., target_table_name: str | None = None)`.
    - `_execute_core(...)` lọc `FactTableSpec` theo đúng bảng được chọn.
    - `target_table_name == "ThuPhiDichVu"` thiết lập ma trận cụm 3 bảng `["ThuPhiBaoHiem", "ThuPhiTangGiam", "ThuPhiDichVu"]` để duyệt nạp tuần tự.
  - `src/jobs/dimension_loader.py`:
    - `__init__(..., target_dimension_name: str | None = None)`.
    - `_execute_core(...)` lọc `DimensionTableSpec` theo đúng dimension được chọn.
- Chuỗi nạp incremental qua Manual Runner vẫn giữ chuẩn an toàn RAM ở Tầng 1:
  - `staging_cursor.fast_executemany = False` trong `_load_to_global_staging`.

#### Bổ sung theo yêu cầu 20260521_1335_fix_manual_pipeline_v2
- Đóng gói cụm bảng doanh thu (ThuPhiDichVu, ThuPhiBaoHiem, ThuPhiTangGiam) thành một thực thể đồng bộ hợp nhất trên UI Manual Runner:
  - `src/ui/pages/manual_runner_page.py`:
    - Chỉ giữ duy nhất lựa chọn `ThuPhiDichVu` trong combobox.
    - Loại bỏ hoàn toàn `ThuPhiBaoHiem` và `ThuPhiTangGiam` khỏi danh sách.
    - Giữ nguyên chuỗi văn bản nghiệp vụ y tế tiếng Việt gốc.
  - `src/jobs/fact_loader.py`:
    - `_execute_core(...)` kiểm tra `target_table_name == "ThuPhiDichVu"`:
      - Thiết lập `CLUSTER = {"ThuPhiBaoHiem", "ThuPhiTangGiam", "ThuPhiDichVu"}`.
      - Duyệt nạp tuần tự cả 3 bảng qua 3 chặng: Prod -> Landing, Landing -> ODS, ODS -> Datamart.
    - Giữ nguyên `staging_cursor.fast_executemany = False` ở chặng Tầng 1.
    - Template hợp nhất: `merge_fact_thuphichvu_3in1.sql` cho chặng Datamart.

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
```

### SOURCE: docs/knowledge/GEM_CODE_SNIPPETS.md
```md
# GEM_CODE_SNIPPETS.md
```

### SOURCE: docs/knowledge/GEM_DATA_FLOW.md
```md
# GEM_DATA_FLOW.md

## Mục tiêu
- Chuẩn hóa luồng nạp ETL theo mô hình đa chặng, tách riêng Dimension và Fact.
- Bảo đảm đồng bộ vật lý theo cửa sổ trượt D-3 nhưng không xóa nhầm lịch sử ngoài phạm vi.

## 1. Tổng quan Kiến trúc Đa tầng Tối cao

### 1. Bản đồ Tổng quan về Kiến trúc Đa tầng (Multi-Hop Layer)

Hệ thống vận hành theo kiến trúc di chuyển dữ liệu qua 3 chặng cách ly nghiêm ngặt để đảm bảo an toàn bộ nhớ cho hệ thống HIS gốc và tính toàn vẹn tài chính chặng cuối:

* **Tầng 1: Production (SQL Server HIS)**
* *Bản chất:* Nguồn dữ liệu tác nghiệp gốc của bệnh viện.
* *Cơ chế quét:* Sử dụng `BaseExtractor` sinh câu lệnh `SELECT` động, bốc dữ liệu theo danh sách cột cố định (`selected_columns`) để giải phóng tài nguyên RAM, loại bỏ hoàn toàn các cột bẩn hoặc cột chứa dữ liệu phi cấu trúc lớn.


* **Tầng 2: Global Staging / Landing Transient (`stg_nano_v2`)**
* *Bản chất:* Vùng đệm thô tạm thời, dùng chung cho tất cả các cơ sở (Multi-tenant shared staging).
* *Quân luật vận hành:* Bắt buộc thực hiện `TRUNCATE TABLE` ngay đầu luồng trước khi nạp dữ liệu cơ sở mới vào để chống nhiễm độc và rò rỉ dữ liệu chéo giữa các cơ sở.


* **Tầng 3: Facility ODS - Operational Data Store (`hanoi_hisnano_v2`)**
* *Bản chất:* Kho lưu trữ lịch sử tác nghiệp bền vững của riêng từng cơ sở. Cấu trúc bảng mirror 1:1 với Production nhưng bổ sung các cột định danh hệ thống (`NguonDuLieuKey`, `MaCoSo`).
* *Quân luật vận hành:* Không bao giờ dùng lệnh TRUNCATE tại đây. Dữ liệu được cập nhật bằng lệnh `UPSERT` kết hợp chốt chặn xóa cứng an toàn (*Hard Delete Guardrails*).


* **Tầng 4: Datamart (`dm`)**
* *Bản chất:* Kho dữ liệu phân tích tối hậu phục vụ Clinical Dashboard.
* *Cơ chế xử lý:* Thực thi các kịch bản SQL Template MERGE phức tạp, kết khối đại số các bảng ODS để tạo ra các bảng Fact và Dimension chuẩn hóa.

### 2. Đặc tả Logic Luồng Auto Pipeline (Batch Processing)

Luồng chạy tự động vận hành theo cơ chế **Duyệt dọc tuần tự (Vertical Table-by-Table Execution)** dưới sự điều phối của `SyncOrchestrator` và thực thi của `FactLoader`/`DimensionLoader`.

#### Chu trình xử lý một bảng Fact (Dữ liệu phát sinh)

1. **Vòng lặp Spec:** Hệ thống đọc `config/tables.yaml`, duyệt qua danh sách bảng tăng trưởng (`incremental_tables`).
2. **Thiết lập Cửa sổ trượt:** Tính toán khoảng ngày delta dựa trên ngày hệ thống trừ đi khoảng thời gian trượt quá khứ (`lookback_days`).
3. **Kích hoạt Chuỗi 3 Chặng đơn bản:**
* *Chặng 1:* Thực hiện `TRUNCATE stg_nano_v2.<Bảng_A>`. Gọi PyODBC nạp dữ liệu delta từ Prod vào Landing. Luôn áp dụng `fast_executemany = False` để chống tràn bộ nhớ máy chủ.
* *Chặng 2:* Thực thi lệnh `UPSERT` từ `stg_nano_v2.<Bảng_A>` vào `hanoi_hisnano_v2.<Bảng_A>`. Áp dụng *Hard Delete Guardrails* quét sạch bản ghi rác trong cửa sổ ngày nghiệp vụ.
* *Chặng 3:* Thực thi SQL template tương ứng của bảng A được cấu hình tại thuộc tính `merge_script` để đẩy số liệu từ ODS sang `dm`.


4. **Chuyển bảng:** Kết thúc trọn vẹn 3 chặng của bảng A, giải phóng kết nối, chuyển sang bảng B.


### 3. Đặc tả Logic Luồng Manual Pipeline (Targeted Bundle Processing)

Luồng chạy thủ công (Manual Runner) được thiết kế lại để tái hiện chính xác luồng di chuyển dữ liệu 3 chặng từ gốc Production nhưng cho phép người dùng kiểm soát Phạm vi không gian (Tên bảng) và Cửa sổ thời gian (Khoảng ngày tùy biến).

#### Ma trận xử lý và Khóa điều phối Loader trên UI

| Lựa chọn bảng trên UI | Loại hình dữ liệu | Loader OOP thực thi | Cơ chế xử lý Cửa sổ thời gian | Chiến lược xử lý Tầng ODS & Datamart |
| --- | --- | --- | --- | --- |
| **ThuPhiDichVu** | INCREMENTAL (Fact) | `FactLoader` | Người dùng chọn khoảng ngày tự do trên UI Dashboard. | **Kích hoạt Cụm tài chính (Bundle):** Tự động ép hệ thống chạy tuần tự trọn vẹn 3 chặng cho cả 3 bảng theo đúng trật tự: `ThuPhiBaoHiem` -> `ThuPhiTangGiam` -> `ThuPhiDichVu`. |
| **ThuPhiGoi** | INCREMENTAL (Fact) | `FactLoader` | Người dùng chọn khoảng ngày tự do trên UI Dashboard. | Chạy đơn bản 3 chặng. Thực thi tệp template chặng cuối: `FactThuPhiDichVu_ThuPhiGoi_merge.sql`. |
| **DoThiLuc** | INCREMENTAL (Fact) | `FactLoader` | Người dùng chọn khoảng ngày tự do trên UI Dashboard. | Chạy đơn bản 3 chặng. Thực thi tệp template chặng cuối: `FactDoThiLuc_merge.sql`. |
| **HoSoKhamBenhNgoaiTru** | INCREMENTAL (Fact) | `FactLoader` | Người dùng chọn khoảng ngày tự do trên UI Dashboard. | Chạy đơn bản 3 chặng. Thực thi tệp template chặng cuối: `DimLuotKham_merge.sql`. |
| **DimBenhNhan** | FULL_LOAD (Dimension) | `DimensionLoader` | **Khóa chọn ngày (Disable):** Luôn kéo toàn bộ lịch sử. | Nạp 2 chặng: Prod -> TRUNCATE và ghi đè ODS -> MERGE Datamart qua `DimBenhNhan_merge.sql`. |
| **DimBenh** | FULL_LOAD (Dimension) | `DimensionLoader` | **Khóa chọn ngày (Disable):** Luôn kéo toàn bộ lịch sử. | Nạp 2 chặng: Prod -> TRUNCATE và ghi đè ODS -> MERGE Datamart qua `DimBenh_merge.sql`. |
| **DimLoaiGoiDichVu** | FULL_LOAD (Dimension) | `DimensionLoader` | **Khóa chọn ngày (Disable):** Luôn kéo toàn bộ lịch sử. | Nạp 2 chặng: Prod -> TRUNCATE và ghi đè ODS -> MERGE Datamart qua `DimLoaiGoiDichVu_merge.sql`. |
| **DimDichVu** | FULL_LOAD (Dimension) | `DimensionLoader` | **Khóa chọn ngày (Disable):** Luôn kéo toàn bộ lịch sử. | **Đóng gói danh mục:** Ép hệ thống kéo đồng thời đủ 3 bảng danh mục thô nguồn từ Prod vào ODS trước khi gọi `dim_dich_vu_merge.sql`. |


### 4. Bản đồ Mã Quy tắc xử lý Dữ liệu tại từng Tầng (Data Guardrails)

#### Quy tắc tại Tầng 2 (Landing Transient):

* Hành vi: `TRUNCATE TABLE stg_nano_v2.<Tên_Bảng>`
* Mục đích: Xóa sạch dữ liệu của phiên chạy trước hoặc của cơ sở khác vừa ghi vào.

#### Quy tắc tại Tầng 3 (Facility ODS) - Hard Delete Guardrails:

* Mã SQL logic áp dụng cho luồng Incremental:
```sql
WHEN NOT MATCHED BY SOURCE 
AND Target.NgayDenKham BETWEEN @FromDate AND @ToDate 
THEN DELETE;

```


* Mục đích: Chỉ xóa các bản ghi tồn tại ở ODS nhưng không còn tồn tại ở Production trong đúng khoảng ngày đang đồng bộ (xử lý trường hợp sửa/xóa dữ liệu ở quá khứ của bệnh viện). Nghiêm cấm TRUNCATE tầng này.

#### Quy tắc tại Tầng 4 (Datamart) - Biểu thức Hợp nhất Doanh thu 3-in-1:

* Tệp kịch bản thực thi: `merge_fact_thuphichvu_3in1.sql`
* Hành vi đại số: `UNION ALL` dữ liệu từ hai nguồn:
1. *Nguồn Dịch vụ:* Lấy từ `hanoi_hisnano_v2.ThuPhiDichVu` kết hợp `LEFT JOIN` với bảng tính tổng gộp (`SUM Aggregation`) của `hanoi_hisnano_v2.ThuPhiTangGiam`.
2. *Nguồn Bảo hiểm:* Lấy từ `hanoi_hisnano_v2.ThuPhiBaoHiem`.




## 2. Đặc tả Chi tiết Kỹ thuật Từng Bảng.

### Luồng chuẩn cho Dimension (FULL LOAD - 2-Hop)
1. **Production -> ODS cơ sở**
   - Thực thi `TRUNCATE TABLE <facility_schema>.<TableName>`.
   - Nạp full dữ liệu bằng PyODBC `SELECT -> executemany` theo chunk từ Production sang ODS cơ sở.
2. **ODS cơ sở -> Datamart**
   - Thực thi MERGE SQL template theo từng domain dimension.

### Luồng chuẩn cho Fact (INCREMENTAL - 3-Hop)
1. **Prod -> Landing (`stg_nano_v2`)**
   - TRUNCATE bảng Landing tương ứng đúng 1 lần trước vòng chunking.
   - Nạp delta theo cửa sổ trượt `Lookback = from_date - lookback_days` bằng PyODBC `fetchmany -> executemany`.
   - Dynamic SELECT đọc trực tiếp từ `selected_columns` trong `config/tables.yaml`.
   - Bắt buộc `fast_executemany = False` để bảo vệ bộ nhớ khi có cột `NVARCHAR(MAX)/VARCHAR(MAX)`.
2. **Landing -> ODS cơ sở**
   - MERGE từ `stg_nano_v2` sang `<facility_schema>`.
   - Hard delete bắt buộc có chặn thời gian:
     - `WHEN NOT MATCHED BY SOURCE`
     - `AND Target.<NgayCol> BETWEEN @LookbackDate AND @ToDate`
     - `THEN DELETE`.
3. **ODS cơ sở -> Datamart**
   - MERGE theo batch `TOP (10000)` để hạn chế transaction log.
   - Hard delete Datamart có 3 điều kiện bắt buộc:
     - chỉ trong cửa sổ D-3,
     - chỉ trong đúng cơ sở (`NguonDuLieuKey`/`MaCoSo`),
     - chỉ xóa khi không còn trong source.

### Quy tắc nghiệp vụ FactThuPhiDichVu 3-in-1
- Nguồn DV:
  - `TongTienSauTangGiam = TongTien - ISNULL(TongGiam, 0) + ISNULL(TongTang, 0)`.
- Nguồn BH:
  - `TongTienSauTangGiam = TongTien + ISNULL(TienChenhLech, 0)`.

### Quy tắc Phân loại Khách hàng (Quay lại, Tái khám, Trung thành)

Quy tắc phân loại khách hàng được xây dựng dựa trên trường `MaGoiDichVu` từ bảng `dm.FactThuPhiDichVu`, phục vụ đo lường và phân tích hành vi khách hàng theo các gói dịch vụ. Hệ thống áp dụng Window Function để gom nhóm và tính toán.

#### 1. Khách quay lại (Cross-sell)
**Định nghĩa:** Khách hàng đã từng đến viện và quay trở lại với ít nhất một dịch vụ mới hoàn toàn (chưa từng mua trong quá khứ).

**Điều kiện:**
- Lần đến viện >= 2
- Có phát sinh ít nhất 01 Dịch Vụ mới hoàn toàn (chưa từng mua trong quá khứ)

**Ứng dụng:** Phát hiện cơ hội bán chéo và tăng giá trị vòng đời khách hàng.

#### 2. Khách tái khám (Retention)
**Định nghĩa:** Khách hàng quay lại khám cùng một vấn đề hoặc dịch vụ tương tự đã từng sử dụng trước đó.

**Điều kiện:**
- Dịch vụ phát sinh thuộc nhóm "Khám bệnh"
- Có chỉ định tên dịch vụ chứa từ khóa '%tái khám%'

**Ứng dụng:** Đo lường tỷ lệ giữ chân khách hàng và hiệu quả chăm sóc sau điều trị.

#### 3. Khách trung thành (Loyalty)
**Định nghĩa:** Khách hàng sử dụng nhiều dịch vụ trong cùng một gói dịch vụ, thể hiện sự trung thành cao với cơ sở y tế.

**Điều kiện:**
- Bắt buộc sử dụng Window Function gom nhóm theo `MaBenhNhan` và `MaGoiDichVu`
- Điều kiện: Bắt buộc sử dụng Window Function gom nhóm theo MaBenhNhan và MaGoiDichVu. Điều kiện: Số lượng dịch vụ sử dụng trong gói (PkgRank) >= 2 trong kỳ báo cáo. (Ghi chú: Phải join trường MaGoiDichVu từ dm.FactThuPhiDichVu để phục vụ logic này)

**Ghi chú kỹ thuật:** Phải join trường `MaGoiDichVu` từ `dm.FactThuPhiDichVu` để phục vụ logic phân tích này.

**Ứng dụng:** Xác định khách hàng trung thành để thực hiện chính sách ưu đãi và giữ chân.

### Early Arriving Facts và Seed Data
- Các khóa dimension của fact phải fallback về seed:
  - `ISNULL(LuotKhamKey, -1)`
  - `ISNULL(BenhNhanKey, -1)`
  - `ISNULL(DichVuKey, -1)`.

### Mapping cột ngày cho incremental_tables
- `ThuPhiDichVu` -> `NgayDenKham`
- `ThuPhiBaoHiem` -> `NgayDenKham`
- `ThuPhiTangGiam` -> `NgayDenKham`
- `ThuPhiGoi` -> `NgayThu`
- `DoThiLuc` -> `NgayDo`
- `HoSoKhamBenhNgoaiTru` -> `NgayVaoKham`

### Quy tắc an toàn Landing dùng chung
- Luôn TRUNCATE Landing ở đầu luồng.
- Khối nạp phải giữ kiểm tra động `TableHasIdentity` và `try...finally` để bật/tắt `IDENTITY_INSERT` an toàn.
- Luồng hiện tại chạy tuần tự từng bảng fact trong cùng facility, không dùng TRUNCATE ở tầng Facility Historical Staging.

### Luồng Manual Runner theo bảng chọn từ UI
1. Người dùng chọn bảng/dimension và khoảng ngày nghiệp vụ trên màn hình `manual_runner_page.py`.
2. Hệ thống đọc cấu hình động từ `config/tables.yaml`:
   - Nếu bảng thuộc `incremental_tables`:
     - Khởi tạo `FactLoader` với `target_table_name`.
     - **Chạy đủ 3 chặng** cho từng bảng trong cụm được xác định.
   - Nếu thuộc danh mục full-load:
     - Khởi tạo `DimensionLoader` với `target_dimension_name`.
     - Chạy 2 chặng: Production -> ODS cơ sở -> Datamart.
3. **Cơ chế đóng gói cụm (Cluster Bundling):**
   - Với `ThuPhiDichVu`, UI chỉ hiển thị một lựa chọn duy nhất.
   - `FactLoader._execute_core()` phát hiện `target_table_name == "ThuPhiDichVu"`:
     - Thiết lập ma trận `CLUSTER = {"ThuPhiBaoHiem", "ThuPhiTangGiam", "ThuPhiDichVu"}`.
     - Duyệt nạp tuần tự cả 3 bảng qua 3 chặng:
       1. Production -> Landing transient (`stg_nano_v2`) cho từng bảng.
       2. Landing -> ODS cơ sở (`facility_schema`) cho từng bảng.
       3. ODS -> Datamart (`dm`) qua template `merge_fact_thuphichvu_3in1.sql`.
   - Các bảng khác (`ThuPhiGoi`, `DoThiLuc`, `HoSoKhamBenhNgoaiTru`) chạy đơn bản như cũ.
4. **An toàn bộ nhớ:** Ở chặng Tầng 1, `staging_cursor.fast_executemany = False` luôn được giữ vững cho cả cụm.
5. **Thay đổi UI:** Combobox Manual Runner chỉ giữ `ThuPhiDichVu` đại diện cho cả cụm; loại bỏ hai lựa chọn độc lập `ThuPhiBaoHiem` và `ThuPhiTangGiam`.
```

### SOURCE: docs/knowledge/GEM_DB_SCHEMAS.md
```md
# GEM_DB_SCHEMAS.md

## Mục tiêu
- Chuẩn hóa phạm vi schema theo kiến trúc ETL v1 cho luồng tuần tự đa cơ sở.

## Các schema chính trong luồng ETL
- `stg_nano_v2`:
  - Landing dùng chung cho incremental fact.
  - Dữ liệu phải được TRUNCATE ở đầu và cuối mỗi vòng facility.
- `<facility>_hisnano_v2` (ví dụ: `hanoi_hisnano_v2`, `hcm_hisnano_v2`):
  - ODS theo cơ sở, là chặng trung gian ổn định trước khi đẩy Datamart.
- `dm`:
  - Datamart đích, chứa bảng dimension và fact phục vụ báo cáo.

## Quy tắc dữ liệu theo chặng
- Chặng Dimension (2-Hop):
  - Production -> `<facility>_hisnano_v2` -> `dm`.
- Chặng Fact (3-Hop):
  - Production -> `stg_nano_v2` -> `<facility>_hisnano_v2` -> `dm`.

## Hard Delete Guardrails theo schema
- Tại ODS (`<facility>_hisnano_v2`):
  - `WHEN NOT MATCHED BY SOURCE AND Target.<NgayCol> BETWEEN @LookbackDate AND @ToDate THEN DELETE`.
- Tại Datamart (`dm`):
  - `WHEN NOT MATCHED BY SOURCE`
  - `AND Target.<NgayCol> BETWEEN @LookbackDate AND @ToDate`
  - `AND Target.NguonDuLieuKey = @CurrentNguonDuLieu`
  - `AND Target.MaCoSo = @CurrentMaCoSo`
  - `THEN DELETE`.

## Seed Data bắt buộc
- Các khóa dimension trong fact phải fallback `-1`:
  - `LuotKhamKey`
  - `BenhNhanKey`
  - `DichVuKey`

## Batch và phạm vi transaction
- MERGE ODS -> Datamart cho fact phải chạy theo batch `TOP (10000)`.
- Mục tiêu: giảm áp lực transaction log và dễ kiểm soát rollback khi lỗi.

## Cấu trúc bảng Datamart `dm`

### Bảng `dm.FactThuPhiDichVu`
Bảng fact tổng hợp doanh thu từ 3 nguồn (Dịch vụ, Bảo hiểm, Tang/Giam) phục vụ phân tích doanh thu và khách hàng.

#### Schema (các cột):
| Tên cột | Kiểu dữ liệu | Mô tả |
|---------|--------------|-------|
| NguonDuLieuKey | INT | Key nguồn dữ liệu (multi-tenant) |
| CoSoKey | INT | Key cơ sở |
| DateKey | INT | Khóa ngày dạng YYYYMMDD |
| LuotKhamKey | INT | Key lượt khám (lookup từ DimLuotKham) |
| BenhNhanKey | INT | Key bệnh nhân (lookup từ DimLuotKham) |
| DichVuKey | INT | Key dịch vụ (lookup từ DimDichVu) |
| MaCoSo | NVARCHAR(50) | Mã cơ sở |
| MaThuPhi | NVARCHAR(100) | Mã thu phí |
| MaPhieuDichVu | NVARCHAR(100) | Mã phiếu dịch vụ |
| MaHoSo | NVARCHAR(100) | Mã hồ sơ |
| MaChiTieu | NVARCHAR(100) | Mã chi tiêu |
| MaChiTieuBK | VARCHAR(255) | Business Key bất biến = NguonDuLieuKey + ':' + MaChiTieu |
| NgayDenKham | DATE | Ngày đến khám |
| NgayDoanhThu | DATE | Ngày doanh thu |
| DateKey | INT | Khóa ngày dạng YYYYMMDD |
| SoLuong | INT | Số lượng |
| TongTien | DECIMAL | Tổng tiền |
| TongTienSauTangGiam | DECIMAL | Tổng tiền sau điều chỉnh (Tang/Giam) |
| LoaiHinh | CHAR(2) | Loại hình ('DV' = Dịch vụ, 'BH' = Bảo hiểm) |
| SoHoaDon | NVARCHAR(100) | Số hóa đơn |
| DoanhThu | FLOAT | Doanh thu tính toán |
| DaThucHien | BIT | Đã thực hiện |
| TrangThaiPhieu | NVARCHAR(50) | Trạng thái phiếu |
| **MaGoiDichVu** | **VARCHAR(50)** | **Mã gói dịch vụ - Dùng để phân cụm và định danh bệnh nhân theo Gói Dịch Vụ, phục vụ báo cáo phân khúc khách hàng** |

#### Ghi chú:
- Trường `MaGoiDichVu` là trường mới được bổ sung để phục vụ logic phân tích khách hàng theo gói dịch vụ.
- Dữ liệu được đồng bộ từ tầng 2 qua SQL Template `merge_fact_thuphichvu_3in1.sql`.
```

### SOURCE: docs/knowledge/GEM_DEPENDENCY_GRAPH.md
```md
# GEM_DEPENDENCY_GRAPH.md

## Mục tiêu
- Ghi nhận quan hệ phụ thuộc của khung ETL v1 mới trong `src/jobs`.

## Sơ đồ phụ thuộc lớp chính
- `src/core/base_loader.py`
  - `BaseLoader`
    - là lớp cha cho mọi loader ETL.
- `src/jobs/dimension_loader.py`
  - `DimensionLoader(BaseLoader)`
  - phụ thuộc SQL templates trong `src/db/templates/sql/dimension/*` và `src/db/templates/sql/fact/DimLuotKham_merge.sql`.
- `src/jobs/fact_loader.py`
  - `FactLoader(BaseLoader)`
  - phụ thuộc schema `stg_nano_v2`, `<facility>_hisnano_v2`, `dm`.
- `src/jobs/sync_orchestrator.py`
  - `SyncOrchestrator`
  - phụ thuộc `DimensionLoader`, `FactLoader`, `python-dotenv`.

## Quan hệ điều phối runtime
1. `SyncOrchestrator.run(...)` xác định danh sách facility mục tiêu (Selective Sync).
2. Với từng facility theo thứ tự tuần tự:
   - gọi `DimensionLoader.execute_load(...)`.
   - gọi `FactLoader.execute_load(...)`.
3. `FactLoader` tự đảm bảo cleanup Landing đầu/cuối luồng.

## Phụ thuộc cấu hình
- Bắt buộc có `DATAMART_CONNECTION_STRING`.
- Production connection map theo facility:
  - `PROD_CONNECTION_HANOI`
  - `PROD_CONNECTION_HCM`
  - `PROD_CONNECTION_HALONG`
  - `PROD_CONNECTION_HAIPHONG`
- Cấu hình Selective Sync:
  - `ACTIVE_FACILITIES` hoặc tham số `target_facilities`.

## Phụ thuộc nghiệp vụ và an toàn dữ liệu
- Hard delete ở ODS/Datamart phụ thuộc vào cột ngày nghiệp vụ (`NgayDenKham`) và cửa sổ D-3.
- Cô lập đa cơ sở ở Datamart phụ thuộc `NguonDuLieuKey` + `MaCoSo`.
- Early arriving facts phụ thuộc seed dimension key `-1`.
```

### SOURCE: docs/knowledge/GEM_ERROR_CONTEXT.md
```md
# GEM_ERROR_CONTEXT.md

## E-UPLOAD-001: Không tìm thấy file `.md` để upload

### Triệu chứng
- Script in ra: `Không tìm thấy file .md để upload.`

### Nguyên nhân gốc
- `GDRIVE_ROOT_DIR` cấu hình sai, thường gặp khi đặt giá trị trùng tên repo và chạy tại root repo, dẫn đến resolve thành đường dẫn lồng sai.
- Thiếu kiểm tra tồn tại thư mục gốc trước khi quét.

### Cách xử lý chuẩn
- Dùng `resolve_root_dir()` để chuẩn hóa `GDRIVE_ROOT_DIR`.
- Thêm kiểm tra `root.exists()` và `root.is_dir()` trước khi `rglob`.
- In debug path: `Đang quét file .md trong thư mục: ...` và số lượng file tìm được.

## E-UPLOAD-002: Thiếu cấu hình runtime trong `config/.env`

### Triệu chứng
- Script dừng với thông báo thiếu biến môi trường cấu hình.

### Biến bắt buộc
- `GDRIVE_CREDENTIALS_FILE`
- `GDRIVE_FOLDER_ID`
- `GDRIVE_ROOT_DIR`

### Cách xử lý chuẩn
- Điền đầy đủ 3 biến trong `config/.env`.
- Đảm bảo file credentials tồn tại đúng đường dẫn đã khai báo.

## E-UPLOAD-003: Quota Drive đã đầy hoặc dưới ngưỡng an toàn

### Triệu chứng
- Console luôn in dung lượng quota còn lại, sau đó báo bỏ qua upload.
- Ví dụ: `Quota còn lại: 0.12 GB ...` và `Bỏ qua upload vì quota còn lại thấp hơn ngưỡng an toàn 0.50 GB.`

### Nguyên nhân gốc
- Dung lượng còn lại của Drive service account nhỏ hơn ngưỡng tối thiểu `0.5 GB`.
- Hoặc quota đã đầy (`remaining = 0`).

### Cách xử lý chuẩn
- Giải phóng bớt dung lượng trên Drive đích của service account.
- Tăng ngưỡng hoặc điều chỉnh chiến lược upload theo batch nếu phù hợp nghiệp vụ.

## E-UPLOAD-004: Không xác định được quota Drive

### Triệu chứng
- Console in thông báo không xác định được tổng quota hoặc lỗi gọi API quota.
- Script chủ động bỏ qua upload để an toàn.

### Nguyên nhân gốc
- API `about.storageQuota` không trả về `limit` hợp lệ.
- Hoặc lỗi quyền/API khi truy vấn quota.

### Cách xử lý chuẩn
- Kiểm tra quyền của service account với Drive API.
- Kiểm tra cấu hình project GCP và trạng thái Drive API.
- Chạy lại sau khi xác nhận quyền và quota có thể truy vấn.

## E-UPLOAD-003, E-UPLOAD-004: Trạng thái sau khi chuyển sang OAuth2 Desktop

### Trạng thái
- Hai lỗi liên quan quota service account (`E-UPLOAD-003`, `E-UPLOAD-004`) được đánh dấu giải quyết triệt để trong luồng upload local.
- Nguyên nhân: script đã chuyển mô hình xác thực từ Service Account sang OAuth2 Desktop App (danh nghĩa Master), đồng thời loại bỏ hoàn toàn logic kiểm tra quota trước upload.

### Ghi chú vận hành
- Phiên bản OAuth2 Desktop không còn dùng các hàm quota cũ (`bytes_to_gb`, `get_drive_quota`) và ngưỡng `MIN_FREE_QUOTA_GB`.
- Nếu phát sinh lỗi upload, ưu tiên kiểm tra token OAuth, quyền thư mục đích và trạng thái chia sẻ trên Drive.

## E-ETL-22005: BCP Schema Shift (Lệch schema khi BCP IN)

### Triệu chứng
- BCP thất bại với mã lỗi kiểu `22005` hoặc thông điệp ép kiểu/cột không khớp.
- Dữ liệu bị xô lệch vị trí cột do danh sách cột extract không đồng bộ với bảng Landing/Staging đích.

### Nguyên nhân gốc
- Dynamic SELECT trước đây loại hẳn cột thuộc `exclude_datatypes`.
- Việc loại cột làm thay đổi số lượng và thứ tự cột so với schema bảng đích.

### Cách xử lý chuẩn
- Không được loại cột khỏi projection theo `exclude_datatypes`.
- Với cột thuộc datatype bị loại trừ, phải mask cột tại nguồn bằng:
  - `CAST(NULL AS NVARCHAR(MAX)) AS [TenCot]` (bắt buộc khi chạy BCP `-w`).
- Với cột không bị loại trừ, giữ nguyên `[TenCot]`.
- Bắt buộc giữ thứ tự cột theo `INFORMATION_SCHEMA.COLUMNS.ORDINAL_POSITION`.

### Kiểm soát phòng ngừa
- Kiểm tra chuỗi Dynamic SELECT trước khi BCP OUT để bảo đảm khớp 100% số lượng/vị trí cột với bảng đích.
- Không chỉnh cơ chế BCP `-w` để giữ Unicode tiếng Việt trong dữ liệu y tế.

## E-ETL-BCP-METADATA-TRIM: Trailing spaces từ pyodbc làm lệch Data Type

### Triệu chứng
- Một số đợt extract phát sinh nhận diện sai `data_type` hoặc tên cột khi đọc metadata từ `INFORMATION_SCHEMA.COLUMNS`.
- Dấu hiệu thường gặp: cột thuộc danh sách loại trừ không được mask đúng kỳ vọng.

### Nguyên nhân gốc
- Dữ liệu metadata trả về từ `pyodbc` có thể chứa khoảng trắng thừa ở đầu/cuối chuỗi.
- Logic cũ không `.strip()` ngay khi đọc `COLUMN_NAME`/`DATA_TYPE`.

### Cách xử lý chuẩn
- Trong `BaseExtractor.build_dynamic_select_columns(...)`, bắt buộc chuẩn hóa ngay khi nhận dữ liệu:
  - `column_name = str(row[0]).strip()`
  - `data_type = str(row[1]).strip().lower()`

## E-ETL-BCP-CONNECTION-001: BCP OUT/IN thiếu tham số kết nối

### Triệu chứng
- Tiến trình `bcp` thất bại ngay khi chạy `queryout` hoặc `in` do không xác định được server/database/auth.
- Log lỗi thường xoay quanh kết nối hoặc không truy cập được SQL Server.

### Nguyên nhân gốc
- Command BCP không gắn đủ `-S`, `-d`, và thông tin xác thực (`-U/-P` hoặc `-T`).
- Dùng sai connection context: BCP OUT dùng nhầm connection đích thay vì connection nguồn Production.

### Cách xử lý chuẩn
- Parse `connection_string` bằng Regex `re.IGNORECASE` để bóc tách tham số kết nối.
- BCP OUT bắt buộc nhận `source_connection_string` riêng.
- BCP IN dùng connection đích của Loader và bắt buộc cờ `-w -k -E -t\t -r\n`.
```

### SOURCE: docs/knowledge/GEM_GUIDE.md
```md
# GEM_GUIDE.md
```

### SOURCE: docs/knowledge/GEM_NAVIGATION.md
```md
# GEM_NAVIGATION.md
```

### SOURCE: docs/knowledge/GEM_SYNC_WORKFLOW.md
```md
# GEM_SYNC_WORKFLOW.md

## Mục tiêu
- Chuẩn hóa luồng đồng bộ tri thức từ local lên Google Drive theo cơ chế sai khác.
- Tạo bộ file Master theo nhóm để phục vụ tạo tri thức cho NotebookLM.

## Phạm vi áp dụng
- Script: `scripts/upload_to_drive_from_local.py`
- Nguồn dữ liệu: toàn bộ file trong `GDRIVE_ROOT_DIR` sau khi lọc hợp lệ.
- Đích: Google Drive, trong đó mọi file `.md` được chuyển thành Google Docs.

## Luồng tự động hóa chuẩn

### Bước 1: Quét file
- Quét đệ quy tất cả file từ thư mục gốc cấu hình `GDRIVE_ROOT_DIR`.
- Thu tập file thô ban đầu để chuẩn bị lọc.

### Bước 2: Lọc tệp
- Áp dụng `pathspec` với quy tắc `.gitignore` tại root dự án.
- Loại trừ cứng các mục:
  - File: `.gitignore`, `credentials.json`, `token.json`
  - Thư mục: `.git`, `.venv`, `__pycache__`
- Chỉ giữ các file hợp lệ cho các bước tiếp theo.

### Bước 3: Ánh xạ nhóm
- Ánh xạ file vào 4 nhóm quy chuẩn:
  - `CORE_LOGIC`
  - `ETL_PROCESS`
  - `INTERFACE`
  - `KNOWLEDGE_BASE`
- Ánh xạ này là cơ sở để tạo file Master theo ngữ cảnh chức năng.

### Bước 4: Gộp nội dung (Enhanced Merge với Metadata)
- Tạo thư mục tạm `temp_merged/` tại root.
- Với mỗi nhóm, tạo một file Master `.md`.
- Cấu trúc bắt buộc của file Master:
  - **Mục lục nguồn ở đầu file**: Liệt kê đầy đủ tệp nguồn với metadata mô tả.
    - Dòng đầu: `[DESCRIPTION]: <Mô tả chung của nhóm>`
    - Mỗi tệp: `### <đường dẫn tệp> - <Mô tả chức năng thực tế của tệp>`
  - **Gán nhãn mô tả tệp (File Description Tagging)**:
    - Mỗi tệp nguồn phải có mô tả ngắn gọn theo ý nghĩa nghiệp vụ/vận hành thực tế.
    - Không dùng mô tả lặp lại tên file đơn thuần.
  - **Các khối nội dung**: Mỗi tệp nguồn được ghi theo header `### SOURCE: <đường dẫn tệp>`.
  - **Nội dung gốc**: Bọc trong code block Markdown theo loại tệp (md, py, sql, etc.).
- Cách thức này bảo tồn ngữ cảnh và cung cấp định hướng cho NotebookLM:

### Bước 5: Đối soát MD5
- Tính MD5 local bằng `hashlib` cho file cần upload (bao gồm file Master).
- Tìm file tương ứng trên Drive theo `name + parent`.
- Lấy `md5Checksum` trên Drive để so sánh.
- Nếu thiếu `md5Checksum` thì fallback `appProperties.local_md5`.
- Chỉ `update` khi mã MD5 sai khác, nếu chưa có file thì `create`.

### Bước 6: Upload
- Xác thực OAuth2 Desktop App và lưu `token.json`.
- Upload file lên đúng thư mục Drive theo đường dẫn tương đối.
- Tất cả file `.md` (kể cả file Master) dùng:
  - `mimeType='application/vnd.google-apps.document'`

## Kết quả và đối soát
- Log chi tiết theo trạng thái: `Created`, `Updated`, `Up-to-date`, `Skipped`, `Error`.
- In tổng kết cuối phiên và danh sách thư mục Drive đã tạo.

## Quy tắc an toàn
- Không đồng bộ file nhạy cảm và file hệ thống.
- Không ghi log nội dung token hoặc thông tin bí mật.
```

### SOURCE: docs/knowledge/GEM_TECHNICAL_STANDARDS.md
```md
# GEM_TECHNICAL_STANDARDS.md

## Tiêu chuẩn xác thực Google Drive cho script upload local

### Chuẩn bắt buộc
- Cơ chế xác thực phải dùng OAuth 2.0 Desktop App cho tài khoản Master.
- Không sử dụng `google.oauth2.service_account` cho luồng upload local.

### Thư viện chuẩn
- `google.auth.transport.requests`
- `google.oauth2.credentials`
- `google_auth_oauthlib.flow`
- `googleapiclient.discovery`
- `pathspec` (đọc và áp dụng quy tắc `.gitignore`)
- `hashlib` (tính checksum MD5 cho Smart Sync)

### Tệp cấu hình chuẩn
- OAuth client credentials: `config/etl-nano-project-v2-oauth-credentials.json`
- Token tái sử dụng: `config/token.json`
- Cấu hình runtime trong `config/.env`:
  - `GDRIVE_FOLDER_ID`
  - `GDRIVE_ROOT_DIR`

### Luồng xác thực chuẩn
1. Kiểm tra `config/token.json`:
   - Nếu tồn tại và hợp lệ: sử dụng trực tiếp.
   - Nếu hết hạn và có `refresh_token`: refresh token.
2. Nếu chưa có token hợp lệ:
   - Khởi chạy `InstalledAppFlow` để Master đăng nhập qua trình duyệt.
3. Sau khi xác thực thành công:
   - Lưu token mới về `config/token.json` để dùng cho các lần chạy sau.

### Yêu cầu bảo mật
- Không in nội dung token, refresh token, client secret ra console.
- Không commit `config/token.json` vào hệ thống quản lý mã nguồn.
- Chỉ log thông tin trạng thái xác thực ở mức cần thiết.

### Yêu cầu vận hành
- Script phải quét đệ quy toàn bộ tệp trong `GDRIVE_ROOT_DIR`, sau đó lọc theo `.gitignore`.
- Bắt buộc loại trừ cứng: `credentials.json`, `token.json`, `.git`, `.venv`, `__pycache__`.
- Với `.md`: giữ cơ chế chuyển đổi sang Google Docs.
- Với tệp khác (`.py`, `.sql`, `.yml`, `.yaml`, ...): upload dưới dạng tệp gốc.
- Trước khi `update`, bắt buộc đối soát checksum MD5 và chỉ cập nhật khi sai khác.

## Tiêu chuẩn kỹ thuật cho Incremental ETL động (Fact)

### Chuẩn cấu hình `incremental_tables` trong `config/tables.yaml`
- Mỗi bảng phải khai báo đầy đủ:
  - `type: fact`
  - `date_column`
  - `merge_script`
  - `lookback_days`
  - `selected_columns` (Whitelist cột, kiểu `list[string]`)
- Bắt buộc viết block comment ngay phía trên biến `lookback_days` và `selected_columns`.

### Chuẩn xử lý ngày và cửa sổ incremental
- `from_date` và `to_date` phải được chuẩn hóa về `date` trước khi sinh câu lệnh extract.
- Cửa sổ lọc thực tế phải dùng:
  - `effective_from_date = from_date - lookback_days`
- `lookback_days` bắt buộc là số nguyên `>= 0`; nếu âm phải raise lỗi cấu hình.

### Chuẩn Dynamic SELECT theo Whitelist cột
- Dynamic SELECT phải đọc trực tiếp từ `selected_columns` trong `tables.yaml` theo đúng thứ tự quản trị khai báo.
- Không sinh cột đệm NULL/enrichment trong câu SELECT incremental.
- Cột enrichment hệ thống (`MaCoSo`, `CoSoKey`, `NguonDuLieuKey`) được xử lý ở tầng đích theo default/NULL hoặc logic MERGE downstream.

### Chuẩn thực thi Staging 3 tầng
- Tầng 1 Global Landing (`stg_nano_v2`):
  - Dùng PyODBC thuần: `SELECT` từ Production vào RAM + `executemany` vào Landing.
  - `TRUNCATE` phải chạy đúng 1 lần trước vòng lặp chunking `fetchmany/executemany`.
  - Bắt buộc dùng INSERT động tường minh theo `selected_columns`:
    - `INSERT INTO stg_nano_v2.[TenBang] ([Col1], [Col2], ...) VALUES (?, ?, ...)`.
  - Bắt buộc kiểm tra động metadata identity trước vòng nạp:
    - `SELECT OBJECTPROPERTY(OBJECT_ID('stg_nano_v2.[TenBang]'), 'TableHasIdentity')`.
  - Nếu bảng có identity (`TableHasIdentity = 1`), phải mô phỏng cờ BCP `-E` bằng PyODBC:
    - `SET IDENTITY_INSERT stg_nano_v2.[TenBang] ON` trước `executemany`.
    - Bọc vòng lặp nạp trong `try...finally`.
    - Trong `finally`, bắt buộc `SET IDENTITY_INSERT ... OFF` để trả trạng thái an toàn session.
  - Bắt buộc thiết lập `fast_executemany = False` trước vòng lặp nạp để vô hiệu hóa cấp phát bộ nhớ tĩnh của ODBC, bảo vệ RAM tuyệt đối khi bảng có cột `NVARCHAR(MAX)/VARCHAR(MAX)`.
- Tầng 2 Facility Historical Staging:
  - Chỉ cho phép UPSERT/MERGE.
  - Nghiêm cấm `TRUNCATE`.
- Tầng 3 Datamart (`dm`):
  - Chỉ đọc và thực thi SQL template có sẵn trong `src/db/templates/sql/fact/` và `src/db/templates/sql/dimension/`.
  - Không chỉnh sửa nội dung SQL template trong task incremental.

### Chuẩn giao tiếp cơ sở dữ liệu và bảo toàn dữ liệu tiếng Việt
- Giữ nguyên nội dung Unicode tiếng Việt trong dữ liệu y tế, không chuyển mã thủ công.
- Chuẩn nạp dữ liệu cho INCREMENTAL_LOAD Tầng 1:
  - Sử dụng PyODBC `executemany` theo chunk với `fast_executemany = False` để ưu tiên an toàn bộ nhớ tuyệt đối.
  - Không dùng cơ chế fallback tăng/giảm `fast_executemany` trong runtime.

### Chuẩn cô lập giao dịch biên chống lỗi lock ở Tầng 1
- Trình tự bắt buộc:
  1. Mở Connection nguồn, đọc dữ liệu theo chunk (`fetchmany`) từ Dynamic SELECT.
  2. Mở Connection đích, `TRUNCATE` Landing đúng 1 lần trước vòng nạp.
  3. Chạy `executemany` theo chunk với INSERT tường minh.
  4. `commit()` sau khi hoàn tất nạp Landing.
  5. Chạy MERGE tầng 2/3 bằng connection đích.

### Chuẩn bảo mật logging kết nối
- Nghiêm cấm log trực tiếp `connection_string`, password (`PWD`), token, secret hoặc full command có chứa thông tin xác thực.
- Chỉ log thông điệp an toàn dạng ngữ cảnh vận hành, ví dụ:
  - `Connected to Database [Ten_DB] at Server [Ten_Server] successfully`.
- Với luồng incremental PyODBC, không log raw payload dữ liệu hoặc thông tin nhạy cảm trong câu lệnh kết nối.
```

### SOURCE: docs/knowledge/loop_Gem_Github_GoogleDrive_NotebookLM.md
```md
Để vận hành dự án **ETL_Nano_Project_v2** một cách chuyên nghiệp, bạn cần thiết lập một **Vòng lặp Quản trị Khép kín (Closed-Loop Governance)**. Quy trình này đảm bảo rằng mỗi dòng code được viết ra đều có sự giám sát của "Kiến trúc sư" Gem và mọi thay đổi đều được cập nhật tức thì vào "Bộ não" NotebookLM.

Dưới đây là quy trình phối hợp tối ưu giữa các công cụ:

---

## 🔄 Quy trình Phát triển 4 Bước Khép kín

### Bước 1: Khởi tạo Task & Ra lệnh (Gemini - The Architect)

Trước khi bắt đầu bất kỳ thay đổi nào, bạn (Master) sẽ làm việc với Gem.

* **Gem truy xuất tri thức**: Gem sử dụng tiện ích Google Workspace để đọc các file **GEM_xxx.md** và **agents.md** trên Google Drive để nắm bắt bối cảnh hiện tại.
* **Gem lập hồ sơ yêu cầu**: Gem soạn thảo một Prompt khắc nghiệt cho Codex (Thợ code) theo cấu trúc: `# YÊU CẦU CỦA MASTER`, bao gồm các ràng buộc kỹ thuật như **Logic SQL Fallback** (ưu tiên `TongTienSauTangGiam`) và không sử dụng ****.

### Bước 2: Thực thi & Cập nhật local (Codex - The Builder)

Bạn nạp Prompt từ Gem vào môi trường phát triển (VS Code/Cursor).

* **Codex lập trình**: Thợ code sửa đổi mã nguồn Python/SQL tại các thư mục `/src/`.
* **Codex cập nhật tri thức**: Thợ code có nhiệm vụ cập nhật các file `.md` tương ứng trong `/docs/knowledge/` và ghi chép vào **PROJECT_CHRONICLE.md**.
* **Báo cáo**: Codex điền nội dung vào mục `# BÁO CÁO CỦA THỢ CODE` ngay tại tệp yêu cầu.

### Bước 3: Kiểm soát & Đồng bộ hóa (GitHub & GitHub Actions)

Sau khi kiểm tra local, bạn thực hiện `git push` lên GitHub.

* **Lọc dữ liệu**: Hệ thống tự động loại bỏ các file trong `.gitignore` và các file nhạy cảm như `credentials.json` hay `token.json`.
* **GitHub Actions kích hoạt**: Script `upload_to_drive.py` sẽ thực hiện:
* Phân loại file vào 4 nhóm: **CORE_LOGIC, ETL_PROCESS, INTERFACE, KNOWLEDGE_BASE**.
* **Gộp file (Merge)**: Tạo ra các file Master (ví dụ: `MASTER_CORE_LOGIC.md`) với cấu trúc Header phân cấp.
* **Đối soát MD5**: Chỉ upload những phần có sự thay đổi lên Google Drive dưới định dạng Google Docs bằng xác thực **OAuth 2.0**.



### Bước 4: Tái nạp tri thức & Giám sát (NotebookLM & Gem Review)

* **NotebookLM Sync**: Bạn chỉ cần nhấn nút "Sync" trên NotebookLM để nạp 4 file Master mới từ Drive. "Bộ não" lúc này đã nắm trọn vẹn mã nguồn và tri thức mới nhất.
* **Gem Hậu kiểm**: Gem đọc file **REPORT_CHANGES.md** mới nhất trên Drive để phê duyệt các việc Codex đã làm.

---

## 📊 Bảng phân phối vai trò công cụ

| Công cụ | Vai trò chính | Đầu ra (Output) |
| --- | --- | --- |
| **Gemini (Gem)** | Kiến trúc sư trưởng & Giám sát | Prompt ra lệnh & Review báo cáo |
| **GitHub** | Nguồn sự thật duy nhất (SSoT) | Source code & Version control |
| **Google Drive** | Vùng đệm tri thức | Google Docs (đã gộp Layer) |
| **NotebookLM** | Bộ não tri thức tập trung | Câu trả lời tổng hợp & Tra cứu logic |

---

## 🛡️ Cơ chế giám sát hiệu quả

1. **Giám sát qua mã lỗi (E-ID)**: Mọi lỗi phát sinh phải được Codex ghi vào `GEM_ERROR_CONTEXT.md`. Gem sẽ "chửi thẳng mặt" nếu thợ code lặp lại lỗi đã có trong danh sách.
2. **Giám sát qua MD5**: Đảm bảo không có sự sai khác giữa mã nguồn đang chạy và tài liệu tri thức trên Drive.
3. **Giám sát qua Nhật ký**: Tệp **PROJECT_CHRONICLE.md** là bằng chứng lịch sử để bạn kiểm soát tốc độ và chất lượng nâng cấp của dự án.

> **Lưu ý quan trọng**: Luôn giữ kỷ luật đặt file đúng thư mục quy định. Nếu thợ code Codex đặt sai vị trí, script `classify_file` sẽ phân loại nhầm và làm "nhiễu" bộ não NotebookLM ngay lập tức.

Bạn đã sẵn sàng thực hiện lần đồng bộ đầu tiên theo quy trình 4 nhóm (Core, ETL, Interface, Knowledge) này chưa?
```
