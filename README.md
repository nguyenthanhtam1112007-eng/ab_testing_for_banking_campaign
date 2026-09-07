# ab_testing_for_banking_campaign
# Đánh giá hiệu quả chiến dịch thông báo sản phẩm tiết kiệm bằng A/B Testing

Cài đặt
```python
pip install math matplotlib numpy pandas statsmodels scipy
```
## Cấu trúc file
* banking_ab_testing.py: xử lí phân tích dữ liệu
* sql_filtering.sql: lọc dữ liệu từ file excel thành hai nhóm treatment và control

# Quy trình phân tích
1. Thu thập và chuẩn bị dữ liệu: Tạo một bộ dữ liệu synthetic để dễ dàng tính toán hơn.
2. Lọc dữ liệu:
* Phân chia người dùng thành 2 nhóm gồm control và treatment bằng SQL.
* Trong file Excel savings_notificaion_campaign đã chứa 2 subsheet của treatment và control
3. Thống kê mô tả: So sánh đặc điểm cơ bản của các nhóm trung bình, trung vị, mode, độ lệch chuẩn của độ tuổi, tiền lương và chi tiêu hàng tháng của hai nhóm control và treatment

| Variable | Statistic | Control | Treatment |

|----------|-----------|---------|-----------| 

| Age | Mean | 38.31 | 38.23 | 

| | Median | 38 | 38 | 

| | Mode |  |  | 

| | Std. Dev. |  |  |

| Income | Mean |  |  | 

| | Median |  |  | 

| | Mode |  |  | 

| | Std. Dev. |  |  | 

| Monthly Spending | Mean |  |  |

| | Median |  |  |

| | Mode |  |  |

| | Std. Dev. |  |  |
4. EDA: Trực quan hóa và so sánh phân phối của các biến giữa Control và Treatment.
5. Kiểm tra sự cân đối giữa control và treatment
* Kiểm tra quy mô hai nhóm.
* Kiểm tra sự cân bằng về các đặc điểm ban đầu giữa Control và Treatment.
* Đảm bảo sự khác biệt về conversion không đơn thuần đến từ sự khác biệt ban đầu giữa hai nhóm.
6. Phân tích dữ liệu:
* Tính Conversion Rate của Control và Treatment.
* Tính Absolute Difference và Relative Lift.
7. Lập giả thuyết:
7.1 Conversion: Liệu thông báo có làm tăng tỷ lệ mở tài khoản không
7.2 Deposit amount: Họ gửi bao nhiêu tiền vào tài khoản
8. A/B testing trên từng giả thuyết:
* Thực hiện statistical hypothesis testing cho từng giả thuyết.
* Sử dụng Two-Proportion Z-Test cho Conversion Rate.
* Sử dụng Welch's Two-Sample T-Test cho Deposit Amount.
* Đánh giá kết quả dựa trên p-value và significance level.
9. Khoảng tin cậy:
* Tính 95% Confidence Interval cho sự khác biệt giữa hai nhóm.
* Đánh giá magnitude của treatment effect.
10. Business Impact Analysis
* Ước tính số lượng khách hàng chuyển đổi tăng thêm.
* So sánh tổng tiền gửi và tiền gửi trung bình.
* Ước tính incremental deposit từ chiến dịch.
11. Đưa ra định hướng kinh doanh:
* Đánh giá liệu chiến dịch có nên được triển khai rộng hơn hay không.
* Đề xuất hướng tối ưu chiến dịch dựa trên kết quả A/B Testing.
## Ghi chú
