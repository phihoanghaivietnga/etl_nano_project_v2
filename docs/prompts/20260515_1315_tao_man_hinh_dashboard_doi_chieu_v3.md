
**# YÊU CẦU CỦA MASTER**

Bạn đã sinh ra mã nguồn nhưng giao diện NiceGUI hoàn toàn tàng hình! Khi khởi chạy `uv run python -m src.ui.main_app` và truy cập trình duyệt, hệ thống chỉ trả về chuỗi JSON của FastAPI: `{"name":"ETL Nano V2 API","version":"1.0.0","status":"running"}`.

Nguyên nhân là do bạn đã tạo các file trong `src/ui/pages/` nhưng lại KHÔNG import chúng vào điểm khởi chạy (entry point) và KHÔNG định tuyến trang chủ.

Bắt buộc thực hiện ngay các hành động khắc phục sau:

**1. Cập nhật `src/ui/main_app.py`:**
- Bắt buộc phải import toàn bộ các trang giao diện đã tạo từ thư mục `pages` (ví dụ: `from src.ui.pages.doi_chieu_page import DoiChieuPage`, `manual_runner_page`, v.v.) để các decorator `@ui.page` được trình biên dịch Python nạp vào bộ nhớ.
- Tạo một hàm định tuyến trang chủ ở đường dẫn gốc:
  ```python
  @ui.page('/')
  def index_page():
      ui.navigate.to('/doi-chieu') # Hoặc điều hướng đến URL của màn hình đối chiếu

```

* Đảm bảo khối lệnh khởi chạy `ui.run(...)` nằm đúng chuẩn ở cuối file.

**2. Rà soát lại các file trong `src/ui/pages/`:**

* Đảm bảo mỗi trang đã có decorator định tuyến rõ ràng (VD: `@ui.page('/doi-chieu')`).

**3. Cập nhật Báo cáo:**

* Sửa mã nguồn ngay lập tức.
* Ghi chú lỗi này và cách khắc phục vào `REPORT_CHANGES.md`.
* Báo cáo kết quả ngay dưới mục # BÁO CÁO CỦA THỢ CODE.

**SMI NGHIÊM NGẶT:** TUYỆT ĐỐI KHÔNG SỬ DỤNG HOẶC HIỂN THỊ BẤT KỲ THẺ CITATION/DẪN NGUỒN NÀO!

**# BÁO CÁO CỦA THỢ CODE**

1) Nguyên nhân lỗi giao diện tàng hình
- Sau khi chạy `uv run python -m src.ui.main_app`, root route chưa điều hướng tới màn hình giao diện và route của các trang chưa được nạp theo cơ chế module-level rõ ràng.
- Kết quả là trình duyệt trả về JSON mặc định của API thay vì trang NiceGUI.

2) Khắc phục trong `src/ui/main_app.py`
- Import tường minh các module pages:
  - `doi_chieu_page`, `manual_runner_page`, `job_history_page`, `bao_cao_page`
- Tạo route gốc:
  - `@ui.page('/')`
  - `ui.navigate.to('/doi-chieu')`
- Giữ đúng block chạy chuẩn ở cuối file:
  - `if __name__ in {"__main__", "__mp_main__"}:`
  - `ui.run(...)`

3) Khắc phục trong các file `src/ui/pages/`
- Chuẩn hóa route mỗi trang bằng decorator tường minh:
  - `@ui.page('/doi-chieu')`
  - `@ui.page('/manual-runner')`
  - `@ui.page('/job-history')`
  - `@ui.page('/bao-cao')`
- Áp dụng wrapper function an toàn scope: mỗi request khởi tạo instance mới của class page trong hàm route, không dùng instance toàn cục.

4) Đồng bộ điều hướng
- Cập nhật `src/ui/pages/common.py`:
  - Route menu đối chiếu chuyển từ `/` sang `/doi-chieu`.
- Cập nhật `active_route` trong `DoiChieuPage` thành `/doi-chieu`.

5) Cập nhật mô-đun pages
- `src/ui/pages/__init__.py` chuyển sang import module-level để decorators `@ui.page` được nạp ngay khi module được import.

6) Cập nhật báo cáo
- Đã ghi nhận lỗi và cách khắc phục vào `REPORT_CHANGES.md`.