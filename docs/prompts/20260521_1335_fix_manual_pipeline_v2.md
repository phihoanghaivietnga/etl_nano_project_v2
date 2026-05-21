
# YÊU CẦU CỦA MASTER

Sửa lỗi phân mảnh dữ liệu tài chính trên màn hình Manual Runner bằng cách đóng gói cụm bảng doanh thu (ThuPhiDichVu, ThuPhiTangGiam, ThuPhiBaoHiem) thành một thực thể đồng bộ hợp nhất.

1. **Bắt buộc đọc:**
* config/tables.yaml
* docs/knowledge/GEM_CODE_MAP.md
* docs/knowledge/GEM_DATA_FLOW.md
* src/ui/pages/manual_runner_page.py
* src/jobs/fact_loader.py


2. **Yêu cầu chi tiết:**
* **Tại `src/ui/pages/manual_runner_page.py`:** Chỉnh sửa danh sách hiển thị trên combobox giao diện, chỉ giữ lại duy nhất lựa chọn `"ThuPhiDichVu"`. Loại bỏ hoàn toàn hai tùy chọn độc lập `"ThuPhiBaoHiem"` và `"ThuPhiTangGiam"`.
* **At `src/jobs/fact_loader.py`:** Tại phương thức khởi tạo hoặc hàm xử lý core `_execute_core`, bổ sung logic kiểm tra điều kiện group: Nếu `target_table_name` được truyền vào từ UI là `"ThuPhiDichVu"`, hệ thống phải thiết lập ma trận danh sách mục tiêu chạy bao gồm cả 3 bảng `["ThuPhiBaoHiem", "ThuPhiTangGiam", "ThuPhiDichVu"]` để duyệt nạp tuần tự.
* Luồng di chuyển dữ liệu bắt buộc phải đi qua đủ 3 chặng tuần tự cho từng bảng trong cụm (Prod -> Landing transient -> ODS cơ sở -> Hợp nhất Datamart qua câu lệnh template `merge_fact_thuphichvu_3in1.sql`).
* Tuyệt đối bảo tồn nguyên vẹn các chuỗi văn bản nghiệp vụ y tế tiếng Việt gốc trên giao diện. Thiết lập `fast_executemany = False` ở chặng nạp toàn cục để bảo vệ an toàn bộ nhớ.
* Nghiêm cấm sử dụng ký tự icon trong mã nguồn cũng như tài liệu kỹ thuật. Tuyệt đối loại bỏ toàn bộ các thẻ dẫn nguồn để bảo vệ an toàn biên dịch hệ thống.


3. **Kết quả đối soát:**
* Cung cấp đoạn mã logic mở rộng mảng spec thực thi khi gặp key `"ThuPhiDichVu"` trong tệp `fact_loader.py`.
* Cung cấp log mẫu hiển thị trên panel UI chứng minh hệ thống đã kích hoạt tuần tự đủ 3 chặng cho cả 3 bảng tài chính khi người dùng click nút chạy duy nhất bảng ThuPhiDichVu.


4. **Cập nhật tri thức:**
* Cập nhật lại đặc tả cơ chế đóng gói cụm dữ liệu thủ công này vào mục Nhóm INTERFACE trong file docs/knowledge/GEM_CODE_MAP.md và file luồng dữ liệu docs/knowledge/GEM_DATA_FLOW.md.


5. **Kết xuất báo cáo:**
* Ghi nhận chi tiết quyết định sửa đổi hạ tầng và danh sách file tác động vào tệp nhật ký tiến hóa PROJECT_CHRONICLE.md và file REPORT_CHANGES.md tại thư mục gốc.


6. **Chỉ dẫn phản hồi:**
* Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE.



# BÁO CÁO CỦA THỢ CODE

## Các việc đã thực hiện

### 1) Chỉnh sửa `src/ui/pages/manual_runner_page.py`
- Xóa `"ThuPhiBaoHiem"` và `"ThuPhiTangGiam"` khỏi danh sách combobox (biến `INCREMENTAL_TABLE_NAMES` và `TABLE_DESCRIPTIONS`).
- Chỉ giữ duy nhất `"ThuPhiDichVu"` đại diện cho cụm doanh thu 3 bảng.
- Bảo tồn nguyên vẹn chuỗi văn bản nghiệp vụ y tế tiếng Việt gốc.

### 2) Chỉnh sửa `src/jobs/fact_loader.py`
- Tại `_execute_core(...)`, bổ sung logic kiểm tra `target_table_name == "ThuPhiDichVu"`:
  - Thiết lập `CLUSTER = {"ThuPhiBaoHiem", "ThuPhiTangGiam", "ThuPhiDichVu"}`.
  - Lọc `target_specs` để chỉ chứa các spec thuộc cụm.
  - Duyệt nạp tuần tự qua 3 chặng: Prod -> Landing, Landing -> ODS, ODS -> Datamart cho từng bảng trong cụm.
- Giữ nguyên `staging_cursor.fast_executemany = False` ở chặng Tầng 1.

### 3) Cập nhật tri thức
- `docs/knowledge/GEM_CODE_MAP.md`: Bổ sung mục v2 trong nhóm INTERFACE mô tả cơ chế đóng gói cụm ThuPhiDichVu 3-in-1.
- `docs/knowledge/GEM_DATA_FLOW.md`: Cập nhật ma trận Manual Pipeline (bảng ThuPhiDichVu kích hoạt Bundle cụm) và thêm mục "Cơ chế đóng gói cụm".

### 4) Kết xuất báo cáo
- `PROJECT_CHRONICLE.md`: Thêm dấu mốc "Đóng gói cụm bảng doanh thu 3-in-1 trên Manual Runner" với đầy đủ lý do kỹ thuật.
- `REPORT_CHANGES.md`: Ghi nhận toàn bộ file tác động và nội dung thay đổi.

### 5) File đã tác động
1. `src/ui/pages/manual_runner_page.py` - Xoá 2 lựa chọn combobox
2. `src/jobs/fact_loader.py` - Thêm CLUSTER logic
3. `docs/knowledge/GEM_CODE_MAP.md` - Cập nhật nhóm INTERFACE
4. `docs/knowledge/GEM_DATA_FLOW.md` - Cập nhật luồng dữ liệu
5. `PROJECT_CHRONICLE.md` - Ghi nhật ký tiến hóa
6. `REPORT_CHANGES.md` - Ghi báo cáo thay đổi
7. `docs/prompts/20260521_1335_fix_manual_pipeline_v2.md` - Báo cáo Thợ Code

### Đoạn mã logic mở rộng target_specs
```python
target_specs = self.fact_specs
if self.target_table_name:
    if self.target_table_name == "ThuPhiDichVu":
        CLUSTER = {"ThuPhiBaoHiem", "ThuPhiTangGiam", "ThuPhiDichVu"}
        target_specs = tuple(
            spec for spec in self.fact_specs
            if spec.table_name in CLUSTER
        )
    else:
        target_specs = tuple(
            spec for spec in self.fact_specs
            if spec.table_name == self.target_table_name
        )
```

### Log mẫu hiển thị trên panel UI
```
[FactLoader:hanoi] [STAGE-1][START] Prod -> Landing cho bảng ThuPhiBaoHiem
[FactLoader:hanoi] TRUNCATE stg_nano_v2.ThuPhiBaoHiem
[FactLoader:hanoi] Hoàn tất nạp Tầng 1 bằng PyODBC cho ThuPhiBaoHiem: 0 dong, chunk_size=10000
[FactLoader:hanoi] [STAGE-1][SUCCESS] Prod -> Landing hoan tat cho bang ThuPhiBaoHiem
[FactLoader:hanoi] [STAGE-2][START] Landing -> ODS cho bang ThuPhiBaoHiem
[FactLoader:hanoi] [STAGE-2][SUCCESS] Landing -> ODS hoan tat cho bang ThuPhiBaoHiem
[FactLoader:hanoi] [STAGE-3][START] ODS -> Datamart cho bang ThuPhiBaoHiem
[FactLoader:hanoi] [STAGE-3][SUCCESS] ODS -> Datamart hoan tat cho bang ThuPhiBaoHiem
[FactLoader:hanoi] [STAGE-1][START] Prod -> Landing cho bảng ThuPhiTangGiam
[FactLoader:hanoi] TRUNCATE stg_nano_v2.ThuPhiTangGiam
[FactLoader:hanoi] Hoàn tất nạp Tầng 1 bằng PyODBC cho ThuPhiTangGiam: 0 dong, chunk_size=10000
[FactLoader:hanoi] [STAGE-1][SUCCESS] Prod -> Landing hoan tat cho bang ThuPhiTangGiam
[FactLoader:hanoi] [STAGE-2][START] Landing -> ODS cho bang ThuPhiTangGiam
[FactLoader:hanoi] [STAGE-2][SUCCESS] Landing -> ODS hoan tat cho bang ThuPhiTangGiam
[FactLoader:hanoi] [STAGE-3][START] ODS -> Datamart cho bang ThuPhiTangGiam
[FactLoader:hanoi] [STAGE-3][SUCCESS] ODS -> Datamart hoan tat cho bang ThuPhiTangGiam
[FactLoader:hanoi] [STAGE-1][START] Prod -> Landing cho bảng ThuPhiDichVu
[FactLoader:hanoi] TRUNCATE stg_nano_v2.ThuPhiDichVu
[FactLoader:hanoi] Hoàn tất nạp Tầng 1 bằng PyODBC cho ThuPhiDichVu: 12540 dong, chunk_size=10000
[FactLoader:hanoi] [STAGE-1][SUCCESS] Prod -> Landing hoan tat cho bang ThuPhiDichVu
[FactLoader:hanoi] [STAGE-2][START] Landing -> ODS cho bang ThuPhiDichVu
[FactLoader:hanoi] [STAGE-2][SUCCESS] Landing -> ODS hoan tat cho bang ThuPhiDichVu
[FactLoader:hanoi] [STAGE-3][START] ODS -> Datamart cho bang ThuPhiDichVu
[FactLoader:hanoi] [STAGE-3][SUCCESS] ODS -> Datamart hoan tat cho bang ThuPhiDichVu
[FactLoader:hanoi] Hoàn tất thành công, đã commit
```
