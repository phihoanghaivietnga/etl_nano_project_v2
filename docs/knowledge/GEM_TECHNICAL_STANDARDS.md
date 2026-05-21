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