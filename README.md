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
| | Std. Dev. | 11.55 | 11.55 |
| Income | Mean | 16.58 | 16.64 |
| | Median | 16.50 | 16.60 |
| | Std. Dev. | 6.00 | 6.10 |
| Monthly Spending | Mean | 9.21 | 9.27 |
| | Median | 9.10 | 9.15 |
| | Std. Dev. | 4.96 | 5.02 |

4. EDA: Trực quan hóa và so sánh phân phối của các biến giữa Control và Treatment.
5. Kiểm tra sự cân đối giữa control và treatment
* Kiểm tra quy mô hai nhóm.

  Số lượng mẫu ở control là 17505

  Số lượng mẫu ở treatment là 17495

  Tổng cộng 35.000 mẫu, tỷ lệ là khoảng 50,01% / 49,99% — hai nhóm gần như bằng nhau tuyệt đối. Đây là dấu hiệu tốt cho việc phân bổ ngẫu nhiên (random assignment) đã hoạt động đúng.
  
* Kiểm tra sự cân bằng về các đặc điểm ban đầu giữa Control và Treatment.

Balance Check: Các đặc điểm ban đầu giữa hai nhóm Control và Treatment có sự tương đồng cao. Mean, Median và Standard Deviation của Age, Income và Monthly Spending giữa hai nhóm chỉ có sự chênh lệch nhỏ. Do đó, hai nhóm được xem là tương đối cân bằng về các đặc điểm cơ bản và có thể tiếp tục thực hiện A/B testing để đánh giá hiệu quả của chiến dịch.

* Đảm bảo sự khác biệt về conversion không đơn thuần đến từ sự khác biệt ban đầu giữa hai nhóm.
6. Phân tích dữ liệu:
* Tính Conversion Rate của Control và Treatment.

| Variable | Opened savings | Total | Conversion rate |
|----------|-----------|---------|-----------|
| Control | 3364 | 17505 | 0.192 |
| Treatment | 4493 | 17495 | 0.286 |

* Tính Absolute Difference và Relative Lift.

**Absolute Difference** = Conversion rate treatment - Conversion rate control = 0.093

**Relative Lift** = $$\frac{Absolute Difference}{Conversion rate control}$$ = 0.485

7. Lập giả thuyết:
  
7.1 Conversion: Liệu thông báo có làm tăng tỷ lệ mở tài khoản không?

H₀ (Null Hypothesis): Tỷ lệ mở tài khoản của nhóm Treatment bằng nhóm Control.

$$ H_0: p_T = p_C $$

H₁ (Alternative Hypothesis): Tỷ lệ mở tài khoản của nhóm Treatment cao hơn nhóm Control.

$$ H_1: p_T > p_C $$

Trong đó:

$$\(p_T\)$$: Conversion Rate của Treatment

$$\(p_C\)$$: Conversion Rate của Control

7.2 Deposit amount: Liệu thông báo có làm tăng số tiền khách hàng gửi vào tài khoản hay không?

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
