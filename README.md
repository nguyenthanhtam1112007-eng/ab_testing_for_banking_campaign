# ab_testing_for_banking_campaign
# Đánh giá hiệu quả chiến dịch thông báo sản phẩm tiết kiệm bằng A/B Testing

Cài đặt
```python
pip install matplotlib numpy pandas statsmodels scipy
```
## Cấu trúc file
* banking_ab_testing.py: xử lí phân tích dữ liệu
* savings_notification_campaign_data.xlsx: synthetic dataset chứa dữ liệu Control và Treatment.
* sql_filtering.sql: lọc dữ liệu từ file excel thành hai nhóm Control và Treatment

# Quy trình phân tích
1. Thu thập và chuẩn bị dữ liệu: Tạo một bộ dữ liệu synthetic để dễ dàng tính toán hơn.
2. Lọc dữ liệu:
* Phân chia người dùng thành 2 nhóm gồm Control và Treatment bằng SQL.
* Trong file Excel savings_notification_campaign_data.xlsx đã chứa 2 subsheet của Control và Treatment
3. Thống kê mô tả: So sánh đặc điểm cơ bản của các nhóm trung bình, trung vị, mode, độ lệch chuẩn của độ tuổi, tiền lương và chi tiêu hàng tháng của hai nhóm Control và Treatment

| Variable | Statistic | Control | Treatment |
|----------|-----------|---------|-----------|
| Age | Mean | $38.31$ | $38.23$ |
| | Median | $38$ | $38$ |
| | Std. Dev. | $11.55$ | $11.55$ |
| Income | Mean | $16.58$ | $16.64$ |
| | Median | $16.50$ | $16.60$ |
| | Std. Dev. | $6.00$ | $6.10$ |
| Monthly Spending | Mean | $9.21$ | $9.27$ |
| | Median | $9.10$ | $9.15$ |
| | Std. Dev. | $4.96$ | $5.02$ |

4. EDA: Trực quan hóa và so sánh phân phối của các biến giữa Control và Treatment.
5. Kiểm tra sự cân đối giữa Control và Treatment

* Kiểm tra quy mô hai nhóm.

  Số lượng mẫu ở Control là $17505$

  Số lượng mẫu ở Treatment là $17495$

  Tổng cộng 35.000 mẫu, tỷ lệ là khoảng $50.01\%$/ $49.99\%$ — hai nhóm gần như bằng nhau tuyệt đối. Đây là dấu hiệu tốt cho việc phân bổ ngẫu nhiên (random assignment) đã hoạt động đúng.
  
* Kiểm tra sự cân bằng về các đặc điểm ban đầu giữa Control và Treatment.

Balance Check: Các đặc điểm ban đầu giữa hai nhóm Control và Treatment có sự tương đồng cao. Mean, median và standard deviation của age, income và monthly spending giữa hai nhóm chỉ có sự chênh lệch nhỏ. Do đó, hai nhóm được xem là tương đối cân bằng về các đặc điểm cơ bản và có thể tiếp tục thực hiện A/B testing để đánh giá hiệu quả của chiến dịch.

Phân bổ ngẫu nhiên được giả định trong thiết kế thử nghiệm tổng hợp. Các bước kiểm tra tính cân bằng được thực hiện để đánh giá xem nhóm Kiểm chứng (Control) và nhóm Thử nghiệm (Treatment) có khả năng so sánh được với nhau dựa trên các đặc điểm nền tảng đã quan sát hay không.

* Đảm bảo sự khác biệt về conversion không đơn thuần đến từ sự khác biệt ban đầu giữa hai nhóm.
6. Phân tích dữ liệu:
* Tính conversion rate của Control và Treatment.

| Variable | Opened savings | Total | Conversion rate |
|----------|-----------|---------|-----------|
| Control | $3364$ | $17505$ | $0.192$ |
| Treatment | $4993$ | $17495$ | $0.285$ |
| Total | $7857$ | $35000$ | $0.224$ |

* Tính Absolute Difference và Relative Lift.

**Absolute Difference** = Conversion rate Treatment - Conversion rate Control = $0.093$

**Relative Lift** = $$\frac{Absolute difference}{Conversion rate Control}$$ = $0.485$

7. Lập giả thuyết:
  
  7.1 Conversion: Liệu thông báo có làm tăng tỷ lệ mở tài khoản không?

H₀ (Null Hypothesis): Tỷ lệ mở tài khoản của nhóm Treatment bằng nhóm Control.

$$ H_0: p_T = p_C $$

H₁ (Alternative Hypothesis): Tỷ lệ mở tài khoản của nhóm Treatment cao hơn nhóm Control.

$$ H_1: p_T > p_C $$

$$Z = \frac{p_T - p_C}{\sqrt{p(1-p)\left(\dfrac{1}{n_T} + \dfrac{1}{n_C}\right)}}$$

Trong đó:

$$\(p_T\)$$: Conversion rate của Treatment

$$\(p_C\)$$: Conversion rate của Control

$$(p)$$: Conversion rate của Pool

$$(n_T)$$: Sample size của Treatment

$$(n_C)$$: Sample size của Control

  7.2 Deposit amount: Liệu notification có tạo ra sự khác biệt về số tiền gửi ban đầu trung bình của những khách hàng mở savings hay không?

H₀: Số tiền gửi trung bình của Treatment bằng Control.

$H_0$: $\bar{X}_T$ = $\bar{X}_C$

H₁: Số tiền gửi trung bình của Treatment khác Control.

$H_1$: $\bar{X}_T$ $\neq$ $\bar{X}_C$

$$T = \frac{\bar{X}_T - \bar{X}_C}{\sqrt{\dfrac{s_C^2}{n_C} + \dfrac{s_T^2}{n_T}}}$$

Trong đó:

$\bar{X}_T$: Số tiền gửi trung bình của Treatment

$\bar{X}_C$: Số tiền gửi trung bình của Control

$$s_T^2$$: Phương sai của số tiền gửi trung bình của Treatment

$$s_C^2$$: Phương sai của số tiền gửi trung bình của Control

$$(n_T)$$: Sample size của Treatment

$$(n_C)$$: Sample size của Control

8. A/B testing trên từng giả thuyết:

8.1 Kiểm định giả thuyết conversion (mục 7.1): Sử dụng Two-Proportion Z-Test

Lựa chọn phương pháp kiểm định

Conversion rate được tính dựa trên biến opened_savings, chỉ nhận hai giá trị:

1: Khách hàng mở savings

0: Khách hàng không mở savings

Do đó, conversion rate của mỗi nhóm có bản chất là một tỷ lệ (proportion). Mục tiêu là kiểm tra xem tỷ lệ mở savings của Treatment có cao hơn Control hay không.

Vì vậy, sử dụng two-proportion z-test để so sánh conversion rate giữa hai nhóm độc lập.

**Significance level** : $$\alpha$$ = $0.05$

Nếu p-value < $0.05$ → Bác bỏ $$\(H_0\)$$

Nếu p-value ≥ $0.05$ → Không đủ cơ sở bác bỏ $$H_0$$

Sau khi chạy mô hình, ta thu được các kết quả:

p-value = $2.77\times10^-93$

Z-statistic = $20.45$

Miền bác bỏ của 7.1: ($$u_{1-\alpha}$$; $$+\infty$$) = (1.645; $$+\infty$$)

Z-statistics = $20.45$ $$\in$$ ($1.645$; $$+\infty$$) nên bác bỏ giả thuyết $$H_0$$

p-value = $$2.77\times10^-93$$ < $0.05$ rất nhiều nên cho thấy bằng chứng để bác bỏ $H_0$ rất mạnh

Vậy có thể bác bỏ giả định $H_0$ và có đủ bằng chứng để ủng hộ giả thuyết $H_1$.

8.2 Kiểm định giả thuyết deposit amount (mục 7.2): Sử dụng Welch's Two-Sample T-Test

Lựa chọn phương pháp kiểm định

Deposit amount là biến định lượng liên tục, thể hiện số tiền khách hàng gửi vào sản phẩm savings. Mục tiêu là kiểm tra liệu số tiền gửi trung bình giữa nhóm Treatment và Control có khác nhau hay không.

Do đó, sử dụng Welch's two-sample t-test để so sánh giá trị trung bình của hai nhóm độc lập.

Trong project này, sử dụng Welch's two-sample t-test, vì phương pháp này không yêu cầu giả định phương sai của hai nhóm bằng nhau và phù hợp khi phương sai giữa hai nhóm có thể khác nhau.

|  | Phương sai | Trung bình | Số lượng mẫu |
|----------|-----------|-----------|-----------|
| Treatment | $51.71$ | $11.85$ | $4993$ |
| Control | $31.97$ | $9.85$ | $3364$ |

**Significance level** : $$\alpha$$ = $0.05$

Nếu p-value < $0.05$ → Bác bỏ $$\(H_0\)$$

Nếu p-value ≥ $0.05$ → Không đủ cơ sở bác bỏ $$H_0$$

Sau khi chạy mô hình, ta thu được các kết quả:

p-value = $$1.96\times10^{-45}$$

T-statistic = $14.23$

Miền bác bỏ giả thuyết là ($$-\infty$$, $$t_{1-\frac{\alpha}{2},df}$$) $$\cup$$ ($$t_{1-\frac{\alpha}{2},df}$$, $$+\infty$$) = ($$-\infty$$, $$1.96$$) $$\cup$$ ($$1.96$$, $$+\infty$$)

T-statistic = $14.23$ $$\in$$ ($$-\infty$$, $-1.96$) $$\cup$$ ($$1.96$$, $$+\infty$$) nên bác bỏ $H_0$

p-value = $$1.96\times10^{-45}$$ < $0.05$ rất nhiều nên cho thấy bằng chứng bác bỏ $H_0$ rất mạnh.

Vậy bác bỏ giả thuyết $H_0$ rằng trung bình tiền gửi trong tài khoản của nhóm Treatment bằng với nhóm Control.

9. Statistical Power Analysis

9.1. Sample Size

   Control: $15505$
   
   Treatment: $15495$
   
   Total: $35000$
   
9.2. Minimum Detectable Effect (MDE)

MDE là mức chênh lệch nhỏ nhất giữa Treatment và Control mà thí nghiệm có khả năng phát hiện được với một mức power và significance đã chọn.

Trong thí nghiệm mục 7.1, đây là một two-proportion test sample size khác nhau $n_T$ $\neq$ $n_C$ nên 
	
$$MDE \approx (z_{1-\alpha} + z_{1-\beta})\sqrt{p_C(1-p_C)\left(\frac{1}{n_C}+\frac{1}{n_T}\right)}$$

Với $\alpha$ = $0.05$ và target power = $0.8$ thì $z_{1-\alpha}$ = 1.645 và $z_{1-\beta}$ = 0.842, tính được MDE $\approx$ $0.010$
	
9.3. Achieved Statistical Power
	
Với $\alpha$ = $0.05$, nếu treatment thực sự tạo ra effect bằng mức effect quan sát được, experiment với sample size hiện tại có xác suất phát hiện ra effect đó là bao nhiêu?
	
Achieved power $\approx$ $0.999$

9.4. Type I/ Type II Error

* Type I Error (**$\alpha$**)

Type I Error xảy ra khi bác bỏ $H_0$ trong khi $H_0$ thực tế đúng. Trong context của project, điều này có nghĩa là kết luận rằng notification làm tăng conversion rate trong khi trên thực tế notification không tạo ra sự gia tăng conversion rate.

Với mức ý nghĩa: $\alpha = 0.05$, xác suất mắc Type I Error được kiểm soát ở mức 5% khi $H_0$ thực sự đúng.

* Type II Error (**$\beta$**)

Type II Error xảy ra khi không bác bỏ $H_0$ trong khi $H_1$ thực tế đúng. Trong context của project, điều này có nghĩa là notification thực sự làm tăng conversion rate nhưng thí nghiệm không phát hiện được sự gia tăng này. Statistical Power được định nghĩa là: $Power = 1-\beta$

Do đó: $\beta = 1-Power$

Với target statistical power là 80%: $\beta = 1-0.8 = 0.2 = 20%$

Target Power = 80% → target Type II Error $\beta = 20%$.

Achieved Power $\approx$ 99.9% → achieved Type II Error ($\beta \approx 0.1%$ tại effect size được quan sát.

Điều này cho thấy với sample size hiện tại, thí nghiệm có statistical power rất cao để phát hiện effect size ở mức quan sát được.

9.5. Practical Significance

**Absolute Differebce** = $0.093$

**Relative Lift** = $48.5%$

**MDE** = $0.010$

Ta thấy absolute difference lớn hơn rất nhiều so với MDE, $0.093$ > $0.010$. Điều này có nghĩa experiment có khả năng phát hiện một effect nhỏ khoảng 1 percentage point, trong khi effect quan sát được là $9.3$ percentage points. Hay nói cách khác, experiment đủ nhạy để phát hiện được những thay đổi khá nhỏ trong conversion rate. conversion rate của treatment cao hơn control nhiều hơn mức effect mà experiment được thiết kế để có khả năng phát hiện

10. Confidence Interval:
* Tính 95% confidence interval cho sự khác biệt mục 7.1.

$1$ - $$\frac{\alpha}{2}$$ = $1$ - $$\frac{0.5}{2}$$ = $0.975$

$$u_{1-\frac{\alpha}{2}}$$ = $$u_{0.975}$$ = $1.96$

**Standard Error** = $$\sqrt{\frac{p_t\times(1-p_t)}{n_t}+\frac{p_c\times(1-p_c)}{n_c}}$$

**Confidence interval** = (**Absolute difference** - $u_{0.975}$ $\times$ **Standard error** ; **Absolute difference** + $u_{0.975}$ $\times$ **Standard error**)

**Confidence interval** = ($$0.084$$, $$0.102$$)

Với độ tin cậy $95%$, Treatment làm tăng conversion rate khoảng $8.4–10.2$ percentage points so với Control.

Vì $$0$$ không nằm trong khoảng Confidence interval, vậy nên có thể bác bỏ giả thuyết $$H_0$$

* Tính 95% Confidence Interval cho sự khác biệt mục 7.2.

**Standard error** = $$\sqrt{\frac{s^2_t}{n_t}+\frac{s^2_c}{n_c}}$$

**Confidence interval** = (($$\bar{X_T}$$ - $$\bar{X_C}$$)  - $t_{0.975}$ $\times$ **Standard error** ; ($$\bar{X_T}$$ - $$\bar{X_C}$$) + $t_{0.975}$ $\times$ **Standard error**)

**Confidence interval** = ($1.730$, $2.282$)

Với độ tin cậy 95%, mức chênh lệch trung bình tiền gửi giữa Treatment và Control nằm trong khoảng từ $1.730$ đến $2.282$ triệu VNĐ.

Vì $$0$$ không nằm trong khoảng confidence interval, vậy nên có thể bác bỏ giả thuyết $$H_0$$

* Đánh giá magnitude của treatment effect.

10. Business Impact Analysis
* So sánh tổng tiền gửi và tiền gửi trung bình.

  Tổng tiền gửi của những khách hàng đã mở tài khoản sau chiến dịch của nhóm Control : **Total deposit Control** = $33120$ triệu VNĐ
  
  Tổng tiền gửi của những khách hàng đã mở tài khoản sau chiến dịch của nhóm Treatment: **Total deposit Treatment** = $59174$ triệu VNĐ

  Tiền gửi trung bình của những khách hàng đã mở tài khoản sau chiến dịch của nhóm Control: **Average deposit Control** = $9.845$ triệu VNĐ
  
  Tiền gửi trung bình của những khách hàng đã mở tài khoản sau chiến dịch của nhóm Treatment: **Average deposit Treatment** $11.851$ triệu VNĐ

  Tổng số người dùng chuyển đổi thêm được tạo ra nhờ Treatment so với Control: **Additional converters** = **Absolute difference** $\times$ **$$N_{treatment}$$** $$\approx$$ $1631$ người
  
* Ước tính incremental deposit từ chiến dịch.

	**Incremental deposit** = **Additional converters** * **Average deposit Treatment** = $19328.693$ triệu VNĐ
  
  Với incremental deposit, đây là con số thể hiện business impact sau khi đã hoàn thành chiến dịch notification chứ không mang tính quan hệ nhân quả.
  
11. Đưa ra định hướng kinh doanh:
* Đánh giá liệu chiến dịch có nên được triển khai rộng hơn hay không.
* Đề xuất hướng tối ưu chiến dịch dựa trên kết quả A/B Testing.
## Ghi chú
Project trình bày cách giải quyết bài toán bằng Data/Statistics, chứ chưa chứng minh rằng con số 9.3 pp sẽ xảy ra trong một chiến dịch ngân hàng thật, vì bộ dữ liệu của project là synthetic data
