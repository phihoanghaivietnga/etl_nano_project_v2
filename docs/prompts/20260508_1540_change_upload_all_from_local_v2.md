
# YÊU CẦU CỦA MASTER

**Bắt buộc đọc:**

* `GEM_TECHNICAL_STANDARDS.md` (Để tuân thủ quy chuẩn về tệp tin được phép upload).
* `GEM_SYNC_WORKFLOW.md` (Để cập nhật danh sách đen các tệp tin trong quy trình đồng bộ).
* Tệp mã nguồn `scripts/upload_to_drive_from_local.py`.

**Yêu cầu chi tiết:**

1. **Cập nhật danh sách loại trừ (Blacklist Update):**
* Sửa logic lọc file trong script `scripts/upload_to_drive_from_local.py` để tuyệt đối KHÔNG upload tệp `.gitignore` lên Google Drive.
* Đảm bảo tệp này bị chặn ngay từ vòng quét tệp tin ban đầu, không đợi đến khi tính toán MD5.
* Việc chặn tệp theo tên (như `.gitignore`) phải được thực hiện song song với việc lọc theo nội dung `.gitignore`. Không hiểu nhầm là chỉ cần chặn mỗi tệp `.gitignore` mà quên mất các quy tắc ẩn bên trong tệp đó.


2. **Mở rộng phạm vi an toàn:**
* Ngoài `.gitignore`, hãy kiểm tra và đảm bảo các tệp cấu hình nhạy cảm hoặc không cần thiết sau cũng bị loại trừ: `.gitattributes`, `.python-version`, và các tệp `.env` (nếu có).



4. **Giao thức phản hồi:**
* Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE.



**Kết quả đối soát:**

* Codex phải cung cấp đoạn log chứng minh khi quét qua tệp `.gitignore`, script đã ghi nhận trạng thái "Ignored" hoặc "Excluded".

**Cập nhật tri thức:**

* Cập nhật `GEM_SYNC_WORKFLOW.md`: Bổ sung mục "Danh sách các tệp không đồng bộ" và ghi rõ lý do tại sao không upload các tệp cấu hình hệ thống.

**Kết xuất báo cáo:**

* Cập nhật tệp `REPORT_CHANGES.md` mô tả logic lọc tệp theo tên cụ thể bên cạnh việc lọc theo mẫu của `pathspec`.

# BÁO CÁO CỦA THỢ CODE

## 1) Cập nhật Blacklist theo yêu cầu
- Đã cập nhật trực tiếp trong `scripts/upload_to_drive_from_local.py`.
- Danh sách loại trừ theo tên (blacklist cứng) gồm:
  - `.gitignore`
  - `.gitattributes`
  - `.python-version`
  - `credentials.json`
  - `token.json`
  - tất cả tệp `.env` (ví dụ: `.env`, `.env.local`, `prod.env`)

## 2) Chặn ngay từ vòng quét ban đầu
- Đã tách rõ 2 tập dữ liệu trong `main()`:
  - `all_files`: tập file trước lọc
  - `candidate_files`: tập file sau lọc
- File blacklist được ghi nhận trạng thái `Excluded` và bị loại ở bước lọc ban đầu.
- File bị loại không đi qua bước tính MD5.

## 3) Giữ lọc theo nội dung `.gitignore` song song
- Vẫn duy trì `pathspec` qua các hàm:
  - `load_gitignore_spec()`
  - `classify_skip_reason()`
- Tức là vừa chặn cứng theo tên, vừa chặn theo mẫu trong `.gitignore`.

## 4) Mở rộng phạm vi an toàn
- Đã bổ sung loại trừ cứng:
  - `.gitattributes`
  - `.python-version`
  - các file `.env`

## 5) Cập nhật tri thức
- Đã cập nhật `GEM_SYNC_WORKFLOW.md`:
  - Thêm mục **Danh sách các tệp không đồng bộ**.
  - Nêu rõ lý do không upload tệp cấu hình hệ thống.

## 6) Cập nhật báo cáo
- Đã cập nhật `REPORT_CHANGES.md`:
  - Mô tả logic lọc theo tên cụ thể (blacklist cứng) chạy song song với lọc mẫu `pathspec`.

## 7) Đối soát log `.gitignore`
- Log đối soát khi quét `.gitignore` ghi nhận trạng thái loại trừ:
  - `[Excluded][forced-file:.gitignore] .gitignore`
