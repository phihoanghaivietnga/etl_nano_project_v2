
**# YÊU CẦU CỦA MASTER**
Hệ thống vừa trải qua một đợt cập nhật nghiệp vụ quan trọng liên quan đến Datamart và logic tính toán Khách hàng. Mã nguồn Python không có sự thay đổi, nhưng hạ tầng Datamart và file SQL Template đã được Master chủ động cập nhật. Yêu cầu mày (Codex) phải đóng vai trò là Người quản trị tri thức, thực hiện cập nhật toàn bộ thông tin này vào **ĐÚNG các tệp quy chuẩn** trong hệ thống tài liệu `.md` để đảm bảo tính toàn vẹn của Knowledge Base. Tuyệt đối KHÔNG tự ý tạo thêm file mới.

### 1. Bối cảnh thay đổi (Master đã tự thực hiện):

* Bổ sung trường `MaGoiDichVu` (`VARCHAR(50)`) vào bảng `dm.FactThuPhiDichVu` trên Datamart.
* Cập nhật file SQL Template: `src/db/template/sql/fact/merge_fact_thuphichvu_3in1.sql` để đồng bộ trường `MaGoiDichVu` từ Tầng 2 lên Tầng 3.
* Các bảng Staging Tầng 1, Tầng 2 và file `tables.yaml` đã có sẵn trường này, không cần can thiệp.

### 2. Yêu cầu cập nhật Tài liệu Tri thức (Bắt buộc):

#### 2.1. Cập nhật Đặc tả Schema (`docs/knowledge/GEM_DB_SCHEMAS.md`):

* Tìm đến phần cấu trúc của tầng Datamart (`dm`). Bổ sung thông tin schema cho bảng `dm.FactThuPhiDichVu`: Thêm trường `MaGoiDichVu` (Kiểu: `VARCHAR(50)`).
* Ghi chú ý nghĩa: "Trường dữ liệu bắt buộc dùng để phân cụm và định danh bệnh nhân theo Gói Dịch Vụ, phục vụ báo cáo phân khúc khách hàng."

#### 2.2. Cập nhật Luồng dữ liệu & Nghiệp vụ (`docs/knowledge/GEM_DATA_FLOW.md`):

* Tìm đến mục đặc tả Quy tắc nghiệp vụ (phần đang chứa các quy tắc FactThuPhiDichVu 3-in-1). Bổ sung thêm một mục mới: **Quy tắc Phân loại Khách hàng (Quay lại, Tái khám, Trung thành)**.
* Tóm tắt và ghi nhận rõ 3 quy tắc nghiệp vụ sau:
1. **Khách quay lại (Cross-sell):** Lần đến viện $\ge$ 2 và có phát sinh ít nhất 01 Dịch Vụ mới hoàn toàn (chưa từng mua trong quá khứ).
2. **Khách tái khám (Retention):** Dịch vụ phát sinh thuộc nhóm "Khám bệnh" và có chỉ định tên dịch vụ chứa từ khóa '%tái khám%'.
3. **Khách trung thành (Loyalty):** Bắt buộc sử dụng Window Function gom nhóm theo `MaBenhNhan` và `MaGoiDichVu`. Điều kiện: Số lượng dịch vụ sử dụng trong gói (PkgRank) $\ge$ 2 trong kỳ báo cáo. (Ghi chú: Phải join trường `MaGoiDichVu` từ `dm.FactThuPhiDichVu` để phục vụ logic này).



#### 2.3. Cập nhật Nhật ký Dự án (`PROJECT_CHRONICLE.md`):

* Ghi nhận sự kiện (ADR): "Cập nhật Schema Datamart & Logic Phân loại Khách hàng".
* Nội dung tóm tắt: "Master đã chủ động nâng cấp bảng `dm.FactThuPhiDichVu` (thêm trường `MaGoiDichVu`) và cập nhật template MERGE `merge_fact_thuphichvu_3in1.sql`. Sự thay đổi này nhằm đáp ứng logic gom nhóm bằng Window Function phục vụ đo lường chỉ số Khách hàng Trung Thành. Khung Python Core không thay đổi do luồng Incremental V2 hỗ trợ đồng bộ metadata động."

#### 2.4. Cập nhật Báo cáo (`REPORT_CHANGES.md`):

* Ghi nhận việc Master đã chỉnh sửa file SQL `src/db/template/sql/fact/merge_fact_thuphichvu_3in1.sql`.
* Liệt kê đích danh các tệp `.md` (GEM_DB_SCHEMAS, GEM_DATA_FLOW, PROJECT_CHRONICLE) mà mày vừa thực hiện cập nhật tri thức.

### 3. Chỉ dẫn phản hồi:

Đây là task vụ cập nhật tri thức (Documentation Update). Mày KHÔNG được phép sinh ra bất kỳ đoạn code Python nào. Chỉ cần thực hiện ghi đè nội dung vào các file `.md` đã chỉ định và báo cáo kết quả.

**# BÁO CÁO CỦA THỢ CODE**

