import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import ttest_ind
data = pd.read_excel('savings_notification_campaign_data.xlsx', sheet_name = "savings_notification_campaign")
data1 = pd.read_excel('savings_notification_campaign_data.xlsx', sheet_name = "control")
data2 = pd.read_excel('savings_notification_campaign_data.xlsx', sheet_name = "treatment")

print(data1[["age", "income", "monthly_spending", "avg_balance"]].describe())
print(data2[["age", "income", "monthly_spending", "avg_balance"]].describe())

variables = ["age", "income", "monthly_spending"]

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
    opened_savings_control,
    opened_savings_treatment
]

nobs = [
    data1.shape[0],
    data2.shape[0]
]

z_stat, p_value = proportions_ztest(success, nobs)

print("Z-statistic:", z_stat)
print("P-value:", p_value)
#__________________________
control_deposit = data1[data1["opened_savings"] == 1]["deposit_amount"]
treatment_deposit = data2[data2["opened_savings"] == 1]["deposit_amount"]
t_stat, p_value = ttest_ind(
    control_deposit,
    treatment_deposit,
    equal_var=False
)
print("T-statistic:", t_stat)
print("P-value:", p_value)

se = math.sqrt(
    conversion_rate_treatment * (1 - conversion_rate_treatment) / data2.shape[0]
    +
    conversion_rate_control * (1 - conversion_rate_control) / data1.shape[0]
)
z = 1.96

ci_lower = absolute_difference - z * se
ci_upper = absolute_difference + z * se

print("Absolute Difference:", absolute_difference)
print("95% CI:", ci_lower, "-", ci_upper)
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