/# YÊU CẦU CỦA MASTER

Chuyển đổi chiến lược quét dữ liệu của luồng Auto Pipeline sang mô hình "Chốt sổ cuối ngày" (End-of-Day Batching). Khóa trần thời gian đồng bộ INCREMENTAL, chỉ lấy dữ liệu đến hết 23:59:59 của ngày hôm qua (T-1), tuyệt đối không kéo dữ liệu của ngày hiện tại.

1. **Bắt buộc đọc:**
* docs/knowledge/GEM_AUTO_PIPELINE.md
* src/jobs/sync_orchestrator.py (hoặc tệp entrypoint trigger luồng Auto)
* src/jobs/fact_loader.py


2. **Yêu cầu chi tiết:**
* **Tại `src/jobs/sync_orchestrator.py` (Lớp điều phối Auto Pipeline):** Tìm đến logic tính toán ngày truyền vào cho luồng quét `incremental_tables`. Thay đổi cách khởi tạo tham số thời gian:
* Biến `to_date` phải được gán bằng ngày hôm qua: `date.today() - timedelta(days=1)`.
* Biến `from_date` phải được tính toán dựa trên `to_date` mới trừ đi `lookback_days` trong file `tables.yaml` (nếu có).


* **Không can thiệp vào SQL:** Giữ nguyên mệnh đề `BETWEEN` tại các file SQL Template và cấu trúc hàm tại `FactLoader`. Việc dịch chuyển tham số đầu vào tại Orchestrator đã đủ để giải quyết bài toán mà không làm gãy kiến trúc chặng cuối.
* Tuân thủ nghiêm ngặt chuẩn Code: Bắt buộc import `timedelta` từ thư viện `datetime`. Không sửa đổi bất kỳ logic nào của luồng Manual Pipeline (vì luồng Manual dựa vào input ngày từ UI của người dùng).
* Không sử dụng icon và loại bỏ các thẻ dẫn nguồn trong code.


3. **Kết quả đối soát:**
* Cung cấp đoạn mã Python thể hiện việc tính toán `to_date` và `from_date` mới tại tệp `sync_orchestrator.py`.
* Cung cấp log mẫu chứng minh: Nếu cronjob chạy vào ngày 22/05/2026, hệ thống chỉ truyền tham số ngày từ 20/05/2026 đến 21/05/2026 (giả sử lookback = 1).


4. **Cập nhật tri thức:**
* Bổ sung quy tắc "Chốt sổ cuối ngày (T-1) cho trần thời gian Auto Pipeline" vào tệp `docs/knowledge/GEM_AUTO_PIPELINE.md`.


5. **Kết xuất báo cáo:**
* Ghi nhận quyết định thay đổi Time Window này vào `PROJECT_CHRONICLE.md` và `REPORT_CHANGES.md`.


6. **Chỉ dẫn phản hồi:**
* Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE.



# BÁO CÁO CỦA THỢ CODE

## Các việc đã thực hiện

### 1) Đọc tài liệu bắt buộc
- `docs/knowledge/GEM_AUTO_PIPELINE.md`: Nắm quy tắc điều phối, luồng gọi loader, cấu hình YAML.
- `src/jobs/sync_orchestrator.py`: Xác định dòng 160: `effective_to_date = to_date or date.today()` va import `from datetime import date`.
- `src/jobs/fact_loader.py`: Xac nhan `_execute_core` nhan `to_date` tu Orchestrator va tinh `from_date` fallback tu `to_date`, sau do `build_extract_plan` ap dung `lookback_days` tu YAML.

### 2) Thay doi ma nguon

**File: `src/jobs/sync_orchestrator.py`**

Thay doi 1: Them `timedelta` vao import.
```python
from datetime import date, timedelta
```

Thay doi 2: Doi logic khoi tao `effective_to_date`.
```python
# Cu:
effective_to_date = to_date or date.today()

# Moi:
effective_to_date = to_date or (date.today() - timedelta(days=1))
print(f"[SyncOrchestrator] Che do chot so T-1: to_date={effective_to_date}")
```

### 3) Khong can thiep
- SQL Template: GIU NGUYEN.
- `FactLoader._execute_core`: GIU NGUYEN.
- `BaseExtractor`: GIU NGUYEN.
- Manual Pipeline: GIU NGUYEN.

### 4) Cap nhat tri thuc
- `docs/knowledge/GEM_AUTO_PIPELINE.md`: Them muc "Quy tac chot so cuoi ngay (T-1)".
- `PROJECT_CHRONICLE.md`: Ghi nhan su kien 2026-05-22 voi day du van de, giai phap, pham vi anh huong.
- `REPORT_CHANGES.md`: Them muc "Pham vi cap nhat theo yeu cau 20260522_0935_change_to_date_auto_pipeline_v1".

### 5) Ket qua doi soat
Chay giao lap cronjob ngay 22/05/2026, lookback=1:
- `to_date` = 21/05/2026 (T-1)
- `from_date` = 21/05/2026 (fallback tu to_date)
- `effective_from_date` = 20/05/2026 (sau khi ap dung lookback_days=1)
- Khoang quet SQL: 20/05/2026 -> 21/05/2026
- Khong lay du lieu ngay hien tai 22/05/2026

Log mau:
```
[SyncOrchestrator] Che do chot so T-1: to_date=2026-05-21
[SyncOrchestrator] Danh sach facility can chay: ['hanoi', 'hcm', ...]