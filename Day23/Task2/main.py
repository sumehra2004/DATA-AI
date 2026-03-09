# ==============================================
# LOAN DEFAULT RISK ANALYSIS (YOUR DATASET)
# ==============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# ==============================================
# LOAD DATA
# ==============================================

print("Loading dataset...")
df = pd.read_csv("loan_data.csv")   # <-- change name if needed

print("\nDataset Shape:", df.shape)
print("\nFirst 5 Rows:\n", df.head())
print("\nData Info:")
print(df.info())

# ==============================================
# PHASE 1: DATA UNDERSTANDING
# ==============================================

print("\nSummary Statistics:\n", df.describe())

print("\nSkewness:\n", df.skew(numeric_only=True))

print("\nDefault Rate (%):",
      round(df["default"].mean()*100, 2))

numerical_cols = df.select_dtypes(include=np.number).columns
categorical_cols = df.select_dtypes(include="object").columns

print("\nNumerical Columns:", list(numerical_cols))
print("Categorical Columns:", list(categorical_cols))

# ==============================================
# PHASE 2: DATA CLEANING
# ==============================================

print("\nMissing Values:\n", df.isnull().sum())

# Drop rows where default is missing
df = df.dropna(subset=["default"])

df["default"] = df["default"].astype(int)

print("Duplicate Rows:", df.duplicated().sum())
df.drop_duplicates(inplace=True)

# ==============================================
# PHASE 3: UNIVARIATE ANALYSIS
# ==============================================

print("\nGenerating Univariate Plots...")

plt.figure()
sns.histplot(df["annual_income"], kde=True)
plt.title("Income Distribution")
plt.savefig("income_distribution.png")
plt.close()

plt.figure()
sns.histplot(df["credit_score"], kde=True)
plt.title("Credit Score Distribution")
plt.savefig("credit_score_distribution.png")
plt.close()

plt.figure()
sns.histplot(df["loan_amount"], kde=True)
plt.title("Loan Amount Distribution")
plt.savefig("loan_amount_distribution.png")
plt.close()

plt.figure()
sns.histplot(df["debt_to_income_ratio"], kde=True)
plt.title("Debt-to-Income Ratio Distribution")
plt.savefig("dti_distribution.png")
plt.close()

plt.figure()
sns.countplot(x="education", data=df)
plt.xticks(rotation=45)
plt.title("Education Distribution")
plt.savefig("education_distribution.png")
plt.close()

# ==============================================
# PHASE 4: BIVARIATE ANALYSIS
# ==============================================

print("\nBivariate Analysis...")

plt.figure()
sns.boxplot(x="default", y="credit_score", data=df)
plt.title("Credit Score vs Default")
plt.savefig("credit_default.png")
plt.close()

plt.figure()
sns.boxplot(x="default", y="debt_to_income_ratio", data=df)
plt.title("DTI vs Default")
plt.savefig("dti_default.png")
plt.close()

plt.figure()
sns.boxplot(x="default", y="late_payments", data=df)
plt.title("Late Payments vs Default")
plt.savefig("late_default.png")
plt.close()

pd.crosstab(df["loan_purpose"], df["default"]).plot(kind="bar", stacked=True)
plt.title("Loan Purpose vs Default")
plt.savefig("purpose_default.png")
plt.close()

# ==============================================
# PHASE 5: MULTIVARIATE ANALYSIS
# ==============================================

plt.figure(figsize=(10,8))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.savefig("correlation_heatmap.png")
plt.close()

print("\nDefault Rate by Loan Purpose:")
print(df.groupby("loan_purpose")["default"].mean())

print("\nDefault Rate by Employment Type:")
print(df.groupby("employment_type")["default"].mean())

# ==============================================
# PHASE 6: OUTLIER DETECTION
# ==============================================

Q1 = df["loan_amount"].quantile(0.25)
Q3 = df["loan_amount"].quantile(0.75)
IQR = Q3 - Q1

outliers = df[(df["loan_amount"] < Q1 - 1.5*IQR) |
              (df["loan_amount"] > Q3 + 1.5*IQR)]

print("\nExtreme Loan Amounts:", len(outliers))

# ==============================================
# PHASE 7: FEATURE ENGINEERING
# ==============================================

df["loan_to_income_ratio"] = df["loan_amount"] / df["annual_income"]

df["risk_score"] = (
    (850 - df["credit_score"]) * 0.5 +
    df["debt_to_income_ratio"] * 0.3 +
    df["late_payments"] * 2
)

df["income_category"] = pd.cut(
    df["annual_income"],
    bins=[0,40000,100000,1000000],
    labels=["Low","Medium","High"]
)

# ==============================================
# PHASE 8: RISK SEGMENTATION
# ==============================================

df["risk_segment"] = pd.cut(
    df["risk_score"],
    bins=[0,200,400,10000],
    labels=["Low Risk","Medium Risk","High Risk"]
)

print("\nRisk Segment Distribution:")
print(df["risk_segment"].value_counts())

print("\nDefault Rate by Risk Segment:")
print(df.groupby("risk_segment")["default"].mean())

# ==============================================
# FINAL BUSINESS INSIGHTS
# ==============================================

print("\n================ FINAL INSIGHTS ================")

print("\nStrongest Predictor of Default:")
print(df.corr(numeric_only=True)["default"].sort_values(ascending=False))

print("\nRiskiest Loan Purpose:")
print(df.groupby("loan_purpose")["default"].mean().idxmax())

print("\nHighest Risk Segment:")
print(df.groupby("risk_segment")["default"].mean().idxmax())

print("\nOverall Default Rate:",
      round(df["default"].mean()*100,2), "%")

print("\nEDA Completed Successfully!")