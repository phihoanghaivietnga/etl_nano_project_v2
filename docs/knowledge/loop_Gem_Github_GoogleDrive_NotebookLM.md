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
* **Codex cập nhật tri thức**: Thợ code có nhiệm vụ cập nhật các file `.md` tương ứng trong `/docs/v2_knowledge/` và ghi chép vào **PROJECT_CHRONICLE.md**.
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