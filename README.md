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
| Total | 7857 | 35000 | 0.224 |

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

H₀: Số tiền gửi trung bình của Treatment bằng Control.

$$ H_0: \mu_T = \mu_C $$

H₁: Số tiền gửi trung bình của Treatment khác Control.

$$ H_1: \mu_T \neq \mu_C $$

Trong đó:

$$\(\mu_T\)$$: Average Deposit Amount của Treatment

$$\(\mu_C\)$$: Average Deposit Amount của Control

8. A/B testing trên từng giả thuyết:

8.1 Kiểm định giả thuyết Conversion (mục 7.1): Sử dụng Two-Proportion Z-Test

Lựa chọn phương pháp kiểm định

Conversion Rate được tính dựa trên biến opened_savings, chỉ nhận hai giá trị:

1: Khách hàng mở Savings
0: Khách hàng không mở Savings

Do đó, Conversion Rate của mỗi nhóm có bản chất là một tỷ lệ (proportion). Mục tiêu là kiểm tra xem tỷ lệ mở Savings của Treatment có cao hơn Control hay không.

Vì vậy, sử dụng Two-Proportion Z-Test để so sánh Conversion Rate giữa hai nhóm độc lập.

**Significance level** : $$\alpha$$ = 0.05

Nếu p-value < 0.05 → Bác bỏ $$\(H_0\)$$

Nếu p-value ≥ 0.05 → Không đủ cơ sở bác bỏ $$H_0$$
	​
Sau khi chạy mô hình, ta thu được các kết quả:

p-value = $$2.77*10^-93$$

Z-statistic = 20.45

Miền bác bỏ của 7.1: ($$u_{1-\alpha}$$; $$+\infty$$) = (1.645; $$+\infty$$)

Z-statistics = 20.45 $$\in$$ (1.645; $$+\infty$$)

Vậy có thể bác bỏ giả định $$H_0$$ và chấp nhận giả thuyết $$H_1$$.

8.2 Kiểm định giả thuyết Deposit Amount (mục 7.2): Sử dụng Welch's Two-Sample T-Test

Lựa chọn phương pháp kiểm định

Deposit amount là biến định lượng liên tục, thể hiện số tiền khách hàng gửi vào sản phẩm Savings. Mục tiêu là kiểm tra liệu số tiền gửi trung bình giữa nhóm Treatment và Control có khác nhau hay không.

Do đó, sử dụng Independent Two-Sample T-Test để so sánh giá trị trung bình của hai nhóm độc lập.

Trong project này, sử dụng Welch's Two-Sample T-Test, vì phương pháp này không yêu cầu giả định phương sai của hai nhóm bằng nhau và phù hợp khi phương sai giữa hai nhóm có thể khác nhau.

|  | Phương sai | Trung bình | Số lượng mẫu |
|----------|-----------|-----------|-----------|
| Treatment | 51.71 | 11.85 | 4993 |
| Control | 31.97 | 9.85 | 3364 |

**Significance level** : $$\alpha$$ = 0.05

Nếu p-value < 0.05 → Bác bỏ $$\(H_0\)$$

Nếu p-value ≥ 0.05 → Không đủ cơ sở bác bỏ $$H_0$$
	​
Sau khi chạy mô hình, ta thu được các kết quả:

p-value = 1.97

Z-statistic = -14.23

Miền bác bỏ giả thuyết là ($$-\infty$$, $$-u_{1-\frac{\alpha}{2}}$$) $$\cup$$ ($$u_{1+\frac{\alpha}{2}}$$, $$+\infty$$) = ($$-\infty$$, $$1.96$$) $$\cup$$ ($$1.96$$, $$+\infty$$)

Z-statistic = -14.23 $$\in$$ ($$-\infty$$, $$-1.96$$) $$\cup$$ ($$1.96$$, $$+\infty$$)

Vậy bác bỏ giả thuyết $$H_0$$ rằng trung bình tiền gửi trong tài khoản của nhóm Treatment bằng với nhóm Control.

9. Khoảng tin cậy:
* Tính 95% Confidence Interval cho sự khác biệt mục 7.1.

1 - $$\frac{\alpha}{2}$$ = 1 - $$\frac{0.5}{2}$$ = $$0.975$$

$$u_{1-\frac{\alpha}{2}}$$ = $$u_{0.975}$$ = 1.96

**Standard Error** = $$\sqrt{\frac{p_t*(1-p_t)}{n_t}+\frac{p_c*(1-p_c)}{n_c}}$$

**Confidence Level** = (**Absolute Difference** - $$u_{0.975}$$***Standard Error** ; **Absolute Difference** + $$u_{0.975}$$***Standard Error**)

**Confidence Level** = (0.084, 0.102)

Vì 0 không nằm trong khoảng Confidence level, vậy nên có thể bác bỏ giả thuyết $$H_0$$

* Tính 95% Confidence Interval cho sự khác biệt mục 7.2.

**Standard Error** = $$\sqrt{\frac{s^2_t}{n_t}+\frac{s^2_c}{n_c}}$$

**Confidence Level** = (($$\mu_t$$ - $$\mu_c$$)  - $$u_{0.975}$$***Standard Error** ; ($$\mu_t$$ - $$\mu_c$$) + $$u_{0.975}$$***Standard Error**)

**Confidence Level** = (1.730, 2.282)

* Đánh giá magnitude của treatment effect.
10. Business Impact Analysis
* Ước tính số lượng khách hàng chuyển đổi tăng thêm.
* So sánh tổng tiền gửi và tiền gửi trung bình.
* Ước tính incremental deposit từ chiến dịch.
11. Đưa ra định hướng kinh doanh:
* Đánh giá liệu chiến dịch có nên được triển khai rộng hơn hay không.
* Đề xuất hướng tối ưu chiến dịch dựa trên kết quả A/B Testing.
## Ghi chú
