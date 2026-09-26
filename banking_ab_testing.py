import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import ttest_ind
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

data = pd.read_excel('savings_notification_campaign_data.xlsx', sheet_name = "savings_notification_campaign")
data1 = pd.read_excel('savings_notification_campaign_data.xlsx', sheet_name = "control")
data2 = pd.read_excel('savings_notification_campaign_data.xlsx', sheet_name = "treatment")

#print(data1[["age", "income", "monthly_spending", "avg_balance"]].describe())
#print(data2[["age", "income", "monthly_spending", "avg_balance"]].describe())

print(f"Phương sai của treatment: {(data2[data2["opened_savings"] == 1]["deposit_amount"].std())**2}")
print(f"Phương sai của control: {(data1[data1["opened_savings"] == 1]["deposit_amount"].std())**2}")
print(f"Trung bình của treatment: {data2[data2["opened_savings"] == 1]["deposit_amount"].mean()}")
print(f"Trung bình của control: {data1[data1["opened_savings"] == 1]["deposit_amount"].mean()}")
print(f"Số lượng mẫu control: {len(data1[data1["opened_savings"] == 1]["deposit_amount"])}")
print(f"Số lượng mẫu treatment: {len(data2[data2["opened_savings"] == 1]["deposit_amount"])}")

var_treatment = (data2[data2["opened_savings"] == 1]["deposit_amount"].std())**2
var_control = (data1[data1["opened_savings"] == 1]["deposit_amount"].std())**2
mean_treatment = data2[data2["opened_savings"] == 1]["deposit_amount"].mean()
mean_control = data1[data1["opened_savings"] == 1]["deposit_amount"].mean()
num_control = len(data1[data1["opened_savings"] == 1]["deposit_amount"])
num_treatment = len(data2[data2["opened_savings"] == 1]["deposit_amount"])
mean_difference = mean_treatment - mean_control
print(f"Mean difference: {mean_difference}") 
variables = ["age", "income", "monthly_spending"]

s_pooled = math.sqrt(((num_control - 1) * var_control + (num_treatment - 1) * var_treatment) / (num_control + num_treatment - 2))

for variable in variables:

    plt.figure(figsize=(8, 5))

    sns.histplot(
        data1,
        x=variable,
        label="Control",
        kde=True,
        alpha=0.5
    )

    sns.histplot(
        data2,
        x=variable,
        label="Treatment",
        kde=True,
        alpha=0.5
    )

    plt.title(f"{variable.capitalize()} Distribution: Treatment vs Control")
    plt.xlabel(variable.capitalize())
    plt.ylabel("Count")
    plt.legend()
    plt.show()

opened_savings_control = data1[data1['opened_savings'] == 1].shape[0]
print(f"open_savings_control: {opened_savings_control}")
conversion_rate_control = opened_savings_control / data1.shape[0]
print(f"conversion_rate_control: {conversion_rate_control}")
opened_savings_treatment = data2[data2['opened_savings'] == 1].shape[0]
print(f"open_savings_treatment: {opened_savings_treatment}")
conversion_rate_treatment = opened_savings_treatment / data2.shape[0]
print(f"conversion_rate_treatment: {conversion_rate_treatment}")
absolute_difference = conversion_rate_treatment - conversion_rate_control
print(f"absolute_difference: {absolute_difference}")
relative_lift = absolute_difference / conversion_rate_control
print(f"relative_lift: {relative_lift}")

success = [
    opened_savings_treatment,
    opened_savings_control
]

nobs = [
    data2.shape[0],
    data1.shape[0]
]

z_stat, p_value = proportions_ztest(success, nobs, alternative = "larger")

print("Z-statistic của two-proportion-z-test:", z_stat)
print("P-value:", p_value)
#__________________________
control_deposit = data1[data1["opened_savings"] == 1]["deposit_amount"]
treatment_deposit = data2[data2["opened_savings"] == 1]["deposit_amount"]
t_stat, p_value = ttest_ind(
    treatment_deposit,
    control_deposit,
    equal_var=False
)
print("T-statistic của two-sample-t-test:", t_stat)
print("P-value:", p_value)

se1 = math.sqrt(
    conversion_rate_treatment * (1 - conversion_rate_treatment) / data2.shape[0]
    +
    conversion_rate_control * (1 - conversion_rate_control) / data1.shape[0]
)
z = 1.96

ci_lower1 = absolute_difference - z * se1
ci_upper1 = absolute_difference + z * se1

print("Absolute Difference:", absolute_difference)
print("95% CI:", ci_lower1, "-", ci_upper1)

se2 = math.sqrt(var_control/num_control + var_treatment/num_treatment)
ci_lower2 = (mean_treatment - mean_control) - z * se2
ci_upper2 = (mean_treatment - mean_control) + z * se2
print("Mean Difference:", mean_treatment - mean_control)
print("95% CI:", ci_lower2, "-", ci_upper2)

#______________________
total_deposit_control = data1[data1["opened_savings"] == 1]["deposit_amount"].sum()
total_deposit_treatment = data2[data2["opened_savings"] == 1]["deposit_amount"].sum()
avg_deposit_control = data1[data1["opened_savings"] == 1]["deposit_amount"].mean()
avg_deposit_treatment = data2[data2["opened_savings"] == 1]["deposit_amount"].mean()
print(f"Total Deposit Control: {total_deposit_control} triệu VNĐ")
print(f"Total Deposit Treatment: {total_deposit_treatment} triệu VNĐ")
print(f"Average Deposit Control: {avg_deposit_control} triệu VNĐ")
print(f"Average Deposit Treatment: {avg_deposit_treatment} triệu VNĐ")
additional_converters = absolute_difference * data2.shape[0]
print(f"Additional Converters: {additional_converters}")
incremental_deposit = additional_converters * avg_deposit_treatment
print(f"Incremental Deposit: {incremental_deposit} triệu VNĐ")

mde = (1.645 + 0.842)*math.sqrt(conversion_rate_control * (1 - conversion_rate_control) * (1/data1.shape[0] + 1/data2.shape[0]))
print(f"MDE: {mde}")

effect_size = proportion_effectsize(conversion_rate_treatment, conversion_rate_control)

power = NormalIndPower().solve_power(
    effect_size=effect_size,
    nobs1=num_treatment,
    alpha=0.05,
    ratio=num_control / num_treatment,
    alternative='larger'
)

print(f"Power: {power}")