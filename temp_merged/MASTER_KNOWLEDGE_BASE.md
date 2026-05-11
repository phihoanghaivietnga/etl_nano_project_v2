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

## 4. Cấu trúc thư mục
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
```

### SOURCE: docs/knowledge/GEM_CODE_SNIPPETS.md
```md
# GEM_CODE_SNIPPETS.md
```

### SOURCE: docs/knowledge/GEM_DATA_FLOW.md
```md
# GEM_DATA_FLOW.md
```

### SOURCE: docs/knowledge/GEM_DB_SCHEMAS.md
```md
# GEM_DB_SCHEMAS.md
```

### SOURCE: docs/knowledge/GEM_DEPENDENCY_GRAPH.md
```md
# GEM_DEPENDENCY_GRAPH.md
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
