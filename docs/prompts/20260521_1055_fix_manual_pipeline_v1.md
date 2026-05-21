
# YÊU CẦU CỦA MASTER

Tái cấu trúc màn hình Manual Runner để thực hiện luồng đồng bộ đa chặng từ gốc Production thay vì gọi lệnh MERGE Datamart chặng cuối đơn thuần, áp dụng cấu hình động theo bảng được chọn và khoảng ngày nghiệp vụ.

1. **Bắt buộc đọc:**
* config/tables.yaml
* docs/knowledge/GEM_CODE_MAP.md
* docs/knowledge/GEM_DATA_FLOW.md
* src/ui/pages/manual_runner_page.py
* src/jobs/fact_loader.py
* src/jobs/dimension_loader.py


2. **Yêu cầu chi tiết:**
* Tại tệp src/ui/pages/manual_runner_page.py: Loại bỏ việc sử dụng GenericTableLoader. Tại hàm run_job, lập luận kiểm tra nếu bảng được chọn nằm trong node incremental_tables của YAML thì khởi tạo FactLoader và truyền tham số ngày từ UI nghiệp vụ vào phương thức execute_load. Nếu bảng thuộc danh mục full-load, khởi tạo DimensionLoader và thực thi nạp toàn bộ.
* Tại tệp src/jobs/fact_loader.py và src/jobs/dimension_loader.py: Cập nhật hàm khởi tạo để tiếp nhận tham số lọc bảng đơn lẻ (target_table_name / target_dimension_name). Ghi đè spec động trong hàm xử lý core để cô lập tiến trình, chỉ thực thi luồng ETL cho bảng được chỉ định từ UI.
* Giữ nguyên các chuỗi văn bản và thuật ngữ y tế tiếng Việt gốc như "nhược thị", "lượt khám", "NgayDenKham", không được tự ý rút gọn thuật ngữ.
* Tuân thủ logic SQL Fallback nghiệp vụ: Chỉ sử dụng trường ThuPhiDichVu.TongTien khi trường ThuPhiDichVu.TongTienSauTangGiam bị NULL.
* Luôn thiết lập fast_executemany = False tại chặng nạp toàn cục để bảo vệ an toàn bộ nhớ.
* Tuyệt đối không sử dụng hoặc hiển thị các thẻ dẫn nguồn có dạng kí tự trong toàn bộ mã nguồn và tài liệu kỹ thuật.


3. **Kết quả đối soát:**
* Yêu cầu Codex cung cấp đoạn mã cấu hình khởi tạo FactLoader động từ manual_runner_page.py và log mẫu tiến trình nạp 3 chặng tuần tự xuất ra terminal khi click nút trên UI.


4. **Cập nhật tri thức:**
* Cập nhật lại kiến trúc điều phối mới của Manual Runner vào mục Nhóm INTERFACE trong file docs/knowledge/GEM_CODE_MAP.md.
* Cập nhật quy trình di chuyển dữ liệu thủ công đi xuyên Landing transient vào file docs/knowledge/GEM_DATA_FLOW.md.


5. **Kết xuất báo cáo:**
* Cập nhật danh sách các file mã nguồn và tài liệu tri thức đã sửa đổi vào tệp nhật ký tiến hóa PROJECT_CHRONICLE.md và file REPORT_CHANGES.md tại thư mục gốc dự án.


6. **Chỉ dẫn phản hồi:**
* Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE.



# BÁO CÁO CỦA THỢ CODE

1) Các việc đã thực hiện
- Đã loại bỏ hoàn toàn `GenericTableLoader` khỏi `src/ui/pages/manual_runner_page.py`.
- Đã chuyển điều phối `run_job` sang cơ chế động theo YAML:
  - Nếu bảng chọn thuộc `incremental_tables` thì khởi tạo `FactLoader` và truyền `from_date/to_date` từ UI vào `execute_load`.
  - Nếu mục chọn thuộc danh mục full-load thì khởi tạo `DimensionLoader` và chạy nạp toàn bộ cho đúng một dimension.
- Đã mở rộng `FactLoader` nhận `target_table_name` và cô lập chạy đúng 1 `FactTableSpec` trong `_execute_core`.
- Đã mở rộng `DimensionLoader` nhận `target_dimension_name` và cô lập chạy đúng 1 `DimensionTableSpec` trong `_execute_core`.
- Đã giữ nguyên chốt an toàn RAM ở Tầng 1 incremental:
  - `staging_cursor.fast_executemany = False`.
- Đã bổ sung log tiến trình 3 chặng tuần tự ở `FactLoader` để đối soát trực tiếp terminal.

2) Đoạn mã cấu hình khởi tạo FactLoader động từ Manual Runner

```python
if self.selected_table in self.incremental_table_names:
    loader = FactLoader(
        datamart_connection=datamart_connection,
        production_connection=production_connection,
        facility_code=facility_code,
        facility_schema=facility_schema,
        nguon_dulieu_key=nguon_dulieu_key,
        co_so_key=co_so_key,
        tables_config_path=str(self.tables_config_path),
        target_table_name=self.selected_table,
    )
    await run.io_bound(
        loader.execute_load,
        from_date_native,
        to_date_native,
        queue=self.log_queue,
        loop=loop,
    )
```

3) Log mẫu tiến trình nạp 3 chặng tuần tự khi click nút UI

```text
[FactLoader:hanoi] [STAGE-1][START] Prod -> Landing cho bảng ThuPhiDichVu
[FactLoader:hanoi] TRUNCATE stg_nano_v2.ThuPhiDichVu
[FactLoader:hanoi] Hoàn tất nạp Tầng 1 bằng PyODBC cho ThuPhiDichVu: 12540 dòng, chunk_size=10000
[FactLoader:hanoi] [STAGE-1][SUCCESS] Prod -> Landing hoàn tất cho bảng ThuPhiDichVu
[FactLoader:hanoi] [STAGE-2][START] Landing -> ODS cho bảng ThuPhiDichVu
[FactLoader:hanoi] [STAGE-2][SUCCESS] Landing -> ODS hoàn tất cho bảng ThuPhiDichVu
[FactLoader:hanoi] [STAGE-3][START] ODS -> Datamart cho bảng ThuPhiDichVu
[FactLoader:hanoi] [STAGE-3][SUCCESS] ODS -> Datamart hoàn tất cho bảng ThuPhiDichVu
[FactLoader:hanoi] Hoàn tất thành công, đã commit
```

4) Cập nhật tri thức và nhật ký
- `docs/knowledge/GEM_CODE_MAP.md`: đã bổ sung kiến trúc điều phối mới của Manual Runner trong nhóm INTERFACE.
- `docs/knowledge/GEM_DATA_FLOW.md`: đã bổ sung luồng manual đi xuyên Landing transient theo bảng chọn.
- `PROJECT_CHRONICLE.md`: đã ghi ADR-39 cho quyết định điều phối động theo bảng chọn.
- `REPORT_CHANGES.md`: đã liệt kê đầy đủ danh sách file mã nguồn và tài liệu đã sửa.