
# YÊU CẦU CỦA MASTER (HIỆU CHỈNH TRI THỨC VÀ LOGIC GỘP)

**Bắt buộc đọc:**

* `GEM_CODE_MAP.md` (Để đối soát lại cấu trúc thư mục).
* `PROJECT_CHRONICLE.md` (Để cập nhật nhật ký hạ tầng).
* `GEM_SYNC_WORKFLOW.md` (Để kiểm tra luồng Enhanced Merge).

**# BƯỚC 1: XÁC NHẬN GIAI ĐOẠN HẠ TẦNG (INFRASTRUCTURE PHASE)**

1. Tôi xác nhận việc các thư mục `/src/core/` và `/src/jobs/` hiện đang trống là **ĐÚNG** ý đồ vì hệ thống đang ưu tiên xây dựng luồng trao đổi tri thức (Gemini - Codex - GitHub - Drive - NotebookLM).
2. Codex không cần tìm cách nạp code nghiệp vụ vào hai nhóm này cho đến khi có yêu cầu tiếp theo.

**# BƯỚC 2: CHUẨN HÓA METADATA VÀ NỘI DUNG MASTER FILE**

1. **Mô tả chức năng thực tế:** Trong mục lục của các file Master, tuyệt đối không được viết theo kiểu lặp lại tên file (ví dụ: `agents.md - agents`). Codex phải viết mô tả ngắn gọn nhưng đầy đủ ý nghĩa (ví dụ: `agents.md - Định nghĩa cấu hình và chiến lược điều phối các AI Agent trong hệ thống`).
2. **Trích xuất bằng chứng (Sample Check):** Sau khi gộp file thành công, Codex phải trích xuất **5 dòng nội dung đầu tiên** bên trong tệp `MASTER_KNOWLEDGE_BASE.md` (phần Header và Mục lục) để Master kiểm tra định dạng.

**# BƯỚC 3: CẬP NHẬT NHẬT KÝ VÀ QUY TRÌNH**

1. **Cập nhật `PROJECT_CHRONICLE.md`:** Ghi rõ mốc thời gian ngày 2026-05-11:
* Hoàn thành thiết lập hạ tầng đồng bộ đa nền tảng.
* Giải trình về số lượng file bị loại (hơn 2200 file) chủ yếu nằm trong thư mục môi trường ảo `.venv`.
* Xác nhận cấu trúc thư mục `/src/` trống là do đang ở giai đoạn xây dựng Pipeline.


2. **Cập nhật `GEM_SYNC_WORKFLOW.md`:** Đảm bảo luồng mô tả việc gộp file Master có bao gồm bước "Gán nhãn mô tả tệp" (File Description Tagging).

**# BƯỚC 4: TRÍCH XUẤT LOG THỰC THI CHUẨN**
Codex phải chạy lại script và cung cấp ít nhất 10 dòng log mới nhất. Log lần này phải chứng minh được:

1. Script đã đứng ở thư mục gốc dự án (`etl_nano_project_v2`) để quét.
2. Log đối soát MD5 cho thấy tệp `MASTER_KNOWLEDGE_BASE.md` đã được cập nhật đầy đủ nội dung từ 15 tệp thành phần.
3. Báo cáo rõ ràng: `CORE_LOGIC: 0 files (Correct for Infra Phase)`.

**# BƯỚC 5: BÁO CÁO VÀ LOG**
Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE.

**# QUY TẮC PHẢN HỒI**

* Tuyệt đối không sử dụng các thẻ dẫn nguồn dạng `` trong nội dung trả về cho Master.
* Ngôn ngữ: Tiếng Việt chuyên nghiệp, ngắn gọn.
* Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE.


# BÁO CÁO CỦA THỢ CODE