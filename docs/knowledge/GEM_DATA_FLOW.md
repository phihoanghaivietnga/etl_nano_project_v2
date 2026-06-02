# GEM_DATA_FLOW.md

## Mục tiêu
- Chuẩn hóa luồng nạp ETL theo mô hình đa chặng, tách riêng Dimension và Fact.
- Bảo đảm đồng bộ vật lý theo cửa sổ trượt D-3 nhưng không xóa nhầm lịch sử ngoài phạm vi.

## 1. Tổng quan Kiến trúc Đa tầng Tối cao

### 1. Bản đồ Tổng quan về Kiến trúc Đa tầng (Multi-Hop Layer)

Hệ thống vận hành theo kiến trúc di chuyển dữ liệu qua 3 chặng cách ly nghiêm ngặt để đảm bảo an toàn bộ nhớ cho hệ thống HIS gốc và tính toàn vẹn tài chính chặng cuối:

* **Tầng 1: Production (SQL Server HIS)**
* *Bản chất:* Nguồn dữ liệu tác nghiệp gốc của bệnh viện.
* *Cơ chế quét:* Sử dụng `BaseExtractor` sinh câu lệnh `SELECT` động, bốc dữ liệu theo danh sách cột cố định (`selected_columns`) để giải phóng tài nguyên RAM, loại bỏ hoàn toàn các cột bẩn hoặc cột chứa dữ liệu phi cấu trúc lớn.


* **Tầng 2: Global Staging / Landing Transient (`stg_nano_v2`)**
* *Bản chất:* Vùng đệm thô tạm thời, dùng chung cho tất cả các cơ sở (Multi-tenant shared staging).
* *Quân luật vận hành:* Bắt buộc thực hiện `TRUNCATE TABLE` ngay đầu luồng trước khi nạp dữ liệu cơ sở mới vào để chống nhiễm độc và rò rỉ dữ liệu chéo giữa các cơ sở.


* **Tầng 3: Facility ODS - Operational Data Store (`hanoi_hisnano_v2`)**
* *Bản chất:* Kho lưu trữ lịch sử tác nghiệp bền vững của riêng từng cơ sở. Cấu trúc bảng mirror 1:1 với Production nhưng bổ sung các cột định danh hệ thống (`NguonDuLieuKey`, `MaCoSo`).
* *Quân luật vận hành:* Không bao giờ dùng lệnh TRUNCATE tại đây. Dữ liệu được cập nhật bằng lệnh `UPSERT` kết hợp chốt chặn xóa cứng an toàn (*Hard Delete Guardrails*).


* **Tầng 4: Datamart (`dm`)**
* *Bản chất:* Kho dữ liệu phân tích tối hậu phục vụ Clinical Dashboard.
* *Cơ chế xử lý:* Thực thi các kịch bản SQL Template MERGE phức tạp, kết khối đại số các bảng ODS để tạo ra các bảng Fact và Dimension chuẩn hóa.

### 2. Đặc tả Logic Luồng Auto Pipeline (Batch Processing)

Luồng chạy tự động vận hành theo cơ chế **Duyệt dọc tuần tự (Vertical Table-by-Table Execution)** dưới sự điều phối của `SyncOrchestrator` và thực thi của `FactLoader`/`DimensionLoader`.

#### Chu trình xử lý một bảng Fact (Dữ liệu phát sinh)

1. **Vòng lặp Spec:** Hệ thống đọc `config/tables.yaml`, duyệt qua danh sách bảng tăng trưởng (`incremental_tables`).
2. **Thiết lập Cửa sổ trượt:** Tính toán khoảng ngày delta dựa trên ngày hệ thống trừ đi khoảng thời gian trượt quá khứ (`lookback_days`).
3. **Kích hoạt Chuỗi 3 Chặng đơn bản:**
* *Chặng 1:* Thực hiện `TRUNCATE stg_nano_v2.<Bảng_A>`. Gọi PyODBC nạp dữ liệu delta từ Prod vào Landing. Luôn áp dụng `fast_executemany = False` để chống tràn bộ nhớ máy chủ.
* *Chặng 2:* Thực thi lệnh `UPSERT` từ `stg_nano_v2.<Bảng_A>` vào `hanoi_hisnano_v2.<Bảng_A>`. Áp dụng *Hard Delete Guardrails* quét sạch bản ghi rác trong cửa sổ ngày nghiệp vụ.
* *Chặng 3:* Thực thi SQL template tương ứng của bảng A được cấu hình tại thuộc tính `merge_script` để đẩy số liệu từ ODS sang `dm`.


4. **Chuyển bảng:** Kết thúc trọn vẹn 3 chặng của bảng A, giải phóng kết nối, chuyển sang bảng B.


### 3. Đặc tả Logic Luồng Manual Pipeline (Targeted Bundle Processing)

Luồng chạy thủ công (Manual Runner) được thiết kế lại để tái hiện chính xác luồng di chuyển dữ liệu 3 chặng từ gốc Production nhưng cho phép người dùng kiểm soát Phạm vi không gian (Tên bảng) và Cửa sổ thời gian (Khoảng ngày tùy biến).

#### Ma trận xử lý và Khóa điều phối Loader trên UI

| Lựa chọn bảng trên UI | Loại hình dữ liệu | Loader OOP thực thi | Cơ chế xử lý Cửa sổ thời gian | Chiến lược xử lý Tầng ODS & Datamart |
| --- | --- | --- | --- | --- |
| **ThuPhiDichVu** | INCREMENTAL (Fact) | `FactLoader` | Người dùng chọn khoảng ngày tự do trên UI Dashboard. | **Kích hoạt Cụm tài chính (Bundle):** Tự động ép hệ thống chạy tuần tự trọn vẹn 3 chặng cho cả 3 bảng theo đúng trật tự: `ThuPhiBaoHiem` -> `ThuPhiTangGiam` -> `ThuPhiDichVu`. |
| **ThuPhiGoi** | INCREMENTAL (Fact) | `FactLoader` | Người dùng chọn khoảng ngày tự do trên UI Dashboard. | Chạy đơn bản 3 chặng. Thực thi tệp template chặng cuối: `FactThuPhiDichVu_ThuPhiGoi_merge.sql`. |
| **DoThiLuc** | INCREMENTAL (Fact) | `FactLoader` | Người dùng chọn khoảng ngày tự do trên UI Dashboard. | Chạy đơn bản 3 chặng. Thực thi tệp template chặng cuối: `FactDoThiLuc_merge.sql`. |
| **HoSoKhamBenhNgoaiTru** | INCREMENTAL (Fact) | `FactLoader` | Người dùng chọn khoảng ngày tự do trên UI Dashboard. | Chạy đơn bản 3 chặng. Thực thi tệp template chặng cuối: `DimLuotKham_merge.sql`. |
| **DimBenhNhan** | FULL_LOAD (Dimension) | `DimensionLoader` | **Khóa chọn ngày (Disable):** Luôn kéo toàn bộ lịch sử. | Nạp 2 chặng: Prod -> TRUNCATE và ghi đè ODS -> MERGE Datamart qua `DimBenhNhan_merge.sql`. |
| **DimBenh** | FULL_LOAD (Dimension) | `DimensionLoader` | **Khóa chọn ngày (Disable):** Luôn kéo toàn bộ lịch sử. | Nạp 2 chặng: Prod -> TRUNCATE và ghi đè ODS -> MERGE Datamart qua `DimBenh_merge.sql`. |
| **DimLoaiGoiDichVu** | FULL_LOAD (Dimension) | `DimensionLoader` | **Khóa chọn ngày (Disable):** Luôn kéo toàn bộ lịch sử. | Nạp 2 chặng: Prod -> TRUNCATE và ghi đè ODS -> MERGE Datamart qua `DimLoaiGoiDichVu_merge.sql`. |
| **DimDichVu** | FULL_LOAD (Dimension) | `DimensionLoader` | **Khóa chọn ngày (Disable):** Luôn kéo toàn bộ lịch sử. | **Đóng gói danh mục:** Ép hệ thống kéo đồng thời đủ 3 bảng danh mục thô nguồn từ Prod vào ODS trước khi gọi `dim_dich_vu_merge.sql`. |


### 4. Bản đồ Mã Quy tắc xử lý Dữ liệu tại từng Tầng (Data Guardrails)

#### Quy tắc tại Tầng 2 (Landing Transient):

* Hành vi: `TRUNCATE TABLE stg_nano_v2.<Tên_Bảng>`
* Mục đích: Xóa sạch dữ liệu của phiên chạy trước hoặc của cơ sở khác vừa ghi vào.

#### Quy tắc tại Tầng 3 (Facility ODS) - Hard Delete Guardrails:

* Mã SQL logic áp dụng cho luồng Incremental:
```sql
WHEN NOT MATCHED BY SOURCE 
AND Target.NgayDenKham BETWEEN @FromDate AND @ToDate 
THEN DELETE;

```


* Mục đích: Chỉ xóa các bản ghi tồn tại ở ODS nhưng không còn tồn tại ở Production trong đúng khoảng ngày đang đồng bộ (xử lý trường hợp sửa/xóa dữ liệu ở quá khứ của bệnh viện). Nghiêm cấm TRUNCATE tầng này.

#### Quy tắc tại Tầng 4 (Datamart) - Biểu thức Hợp nhất Doanh thu 3-in-1:

* Tệp kịch bản thực thi: `merge_fact_thuphichvu_3in1.sql`
* Hành vi đại số: `UNION ALL` dữ liệu từ hai nguồn:
1. *Nguồn Dịch vụ:* Lấy từ `hanoi_hisnano_v2.ThuPhiDichVu` kết hợp `LEFT JOIN` với bảng tính tổng gộp (`SUM Aggregation`) của `hanoi_hisnano_v2.ThuPhiTangGiam`.
2. *Nguồn Bảo hiểm:* Lấy từ `hanoi_hisnano_v2.ThuPhiBaoHiem`.




## 2. Đặc tả Chi tiết Kỹ thuật Từng Bảng.

### Luồng chuẩn cho Dimension (FULL LOAD - 2-Hop)
1. **Production -> ODS cơ sở**
   - Thực thi `TRUNCATE TABLE <facility_schema>.<TableName>`.
   - Nạp full dữ liệu bằng PyODBC `SELECT -> executemany` theo chunk từ Production sang ODS cơ sở.
2. **ODS cơ sở -> Datamart**
   - Thực thi MERGE SQL template theo từng domain dimension.

### Luồng chuẩn cho Fact (INCREMENTAL - 3-Hop)
1. **Prod -> Landing (`stg_nano_v2`)**
   - TRUNCATE bảng Landing tương ứng đúng 1 lần trước vòng chunking.
   - Nạp delta theo cửa sổ trượt `Lookback = from_date - lookback_days` bằng PyODBC `fetchmany -> executemany`.
   - Dynamic SELECT đọc trực tiếp từ `selected_columns` trong `config/tables.yaml`.
   - Bắt buộc `fast_executemany = False` để bảo vệ bộ nhớ khi có cột `NVARCHAR(MAX)/VARCHAR(MAX)`.
2. **Landing -> ODS cơ sở**
   - MERGE từ `stg_nano_v2` sang `<facility_schema>`.
   - Hard delete bắt buộc có chặn thời gian:
     - `WHEN NOT MATCHED BY SOURCE`
     - `AND Target.<NgayCol> BETWEEN @LookbackDate AND @ToDate`
     - `THEN DELETE`.
3. **ODS cơ sở -> Datamart**
   - MERGE theo batch `TOP (10000)` để hạn chế transaction log.
   - Hard delete Datamart có 3 điều kiện bắt buộc:
     - chỉ trong cửa sổ D-3,
     - chỉ trong đúng cơ sở (`NguonDuLieuKey`/`MaCoSo`),
     - chỉ xóa khi không còn trong source.

### Quy tắc nghiệp vụ FactThuPhiDichVu 3-in-1
- Nguồn DV:
  - `TongTienSauTangGiam = TongTien - ISNULL(TongGiam, 0) + ISNULL(TongTang, 0)`.
- Nguồn BH:
  - `TongTienSauTangGiam = TongTien + ISNULL(TienChenhLech, 0)`.

### Quy tắc Phân loại Khách hàng (Quay lại, Tái khám, Trung thành)

Quy tắc phân loại khách hàng được xây dựng dựa trên trường `MaGoiDichVu` từ bảng `dm.FactThuPhiDichVu`, phục vụ đo lường và phân tích hành vi khách hàng theo các gói dịch vụ. Hệ thống áp dụng Window Function để gom nhóm và tính toán.

#### 1. Khách quay lại (Cross-sell)
**Định nghĩa:** Khách hàng đã từng đến viện và quay trở lại với ít nhất một dịch vụ mới hoàn toàn (chưa từng mua trong quá khứ).

**Điều kiện:**
- Lần đến viện >= 2
- Có phát sinh ít nhất 01 Dịch Vụ mới hoàn toàn (chưa từng mua trong quá khứ)

**Ứng dụng:** Phát hiện cơ hội bán chéo và tăng giá trị vòng đời khách hàng.

#### 2. Khách tái khám (Retention)
**Định nghĩa:** Khách hàng quay lại khám cùng một vấn đề hoặc dịch vụ tương tự đã từng sử dụng trước đó.

**Điều kiện:**
- Dịch vụ phát sinh thuộc nhóm "Khám bệnh"
- Có chỉ định tên dịch vụ chứa từ khóa '%tái khám%'

**Ứng dụng:** Đo lường tỷ lệ giữ chân khách hàng và hiệu quả chăm sóc sau điều trị.

#### 3. Khách trung thành (Loyalty)
**Định nghĩa:** Khách hàng sử dụng nhiều dịch vụ trong cùng một gói dịch vụ, thể hiện sự trung thành cao với cơ sở y tế.

**Điều kiện:**
- Bắt buộc sử dụng Window Function gom nhóm theo `MaBenhNhan` và `MaGoiDichVu`
- Điều kiện: Bắt buộc sử dụng Window Function gom nhóm theo MaBenhNhan và MaGoiDichVu. Điều kiện: Số lượng dịch vụ sử dụng trong gói (PkgRank) >= 2 trong kỳ báo cáo. (Ghi chú: Phải join trường MaGoiDichVu từ dm.FactThuPhiDichVu để phục vụ logic này)

**Ghi chú kỹ thuật:** Phải join trường `MaGoiDichVu` từ `dm.FactThuPhiDichVu` để phục vụ logic phân tích này.

**Ứng dụng:** Xác định khách hàng trung thành để thực hiện chính sách ưu đãi và giữ chân.

### Early Arriving Facts và Seed Data
- Các khóa dimension của fact phải fallback về seed:
  - `ISNULL(LuotKhamKey, -1)`
  - `ISNULL(BenhNhanKey, -1)`
  - `ISNULL(DichVuKey, -1)`.

### Mapping cột ngày cho incremental_tables
- `ThuPhiDichVu` -> `NgayDenKham`
- `ThuPhiBaoHiem` -> `NgayDenKham`
- `ThuPhiTangGiam` -> `NgayDenKham`
- `ThuPhiGoi` -> `NgayThu`
- `DoThiLuc` -> `NgayDo`
- `HoSoKhamBenhNgoaiTru` -> `NgayVaoKham`

### Quy tắc an toàn Landing dùng chung
- Luôn TRUNCATE Landing ở đầu luồng.
- Khối nạp phải giữ kiểm tra động `TableHasIdentity` và `try...finally` để bật/tắt `IDENTITY_INSERT` an toàn.
- Luồng hiện tại chạy tuần tự từng bảng fact trong cùng facility, không dùng TRUNCATE ở tầng Facility Historical Staging.

### Luồng Manual Runner theo bảng chọn từ UI
1. Người dùng chọn bảng/dimension và khoảng ngày nghiệp vụ trên màn hình `manual_runner_page.py`.
2. Hệ thống đọc cấu hình động từ `config/tables.yaml`:
   - Nếu bảng thuộc `incremental_tables`:
     - Khởi tạo `FactLoader` với `target_table_name`.
     - **Chạy đủ 3 chặng** cho từng bảng trong cụm được xác định.
   - Nếu thuộc danh mục full-load:
     - Khởi tạo `DimensionLoader` với `target_dimension_name`.
     - Chạy 2 chặng: Production -> ODS cơ sở -> Datamart.
3. **Cơ chế đóng gói cụm (Cluster Bundling):**
   - Với `ThuPhiDichVu`, UI chỉ hiển thị một lựa chọn duy nhất.
   - `FactLoader._execute_core()` phát hiện `target_table_name == "ThuPhiDichVu"`:
     - Thiết lập ma trận `CLUSTER = {"ThuPhiBaoHiem", "ThuPhiTangGiam", "ThuPhiDichVu"}`.
     - Duyệt nạp tuần tự cả 3 bảng qua 3 chặng:
       1. Production -> Landing transient (`stg_nano_v2`) cho từng bảng.
       2. Landing -> ODS cơ sở (`facility_schema`) cho từng bảng.
       3. ODS -> Datamart (`dm`) qua template `merge_fact_thuphichvu_3in1.sql`.
   - Các bảng khác (`ThuPhiGoi`, `DoThiLuc`, `HoSoKhamBenhNgoaiTru`) chạy đơn bản như cũ.
4. **An toàn bộ nhớ:** Ở chặng Tầng 1, `staging_cursor.fast_executemany = False` luôn được giữ vững cho cả cụm.
5. **Thay đổi UI:** Combobox Manual Runner chỉ giữ `ThuPhiDichVu` đại diện cho cả cụm; loại bỏ hai lựa chọn độc lập `ThuPhiBaoHiem` và `ThuPhiTangGiam`.
