# ==========================================
# E-COMMERCE EDA PROJECT (YOUR DATASET)
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler

sns.set(style="whitegrid")

# ==========================================
# LOAD DATA (TAB SEPARATED)
# ==========================================

print("Loading dataset...")

df = pd.read_csv("ecommerce_customer_behavior_dataset.csv")

print("Dataset Shape:", df.shape)
print("\nFirst 5 Rows:\n", df.head())
print("\nData Info:")
print(df.info())

# ==========================================
# DATA UNDERSTANDING
# ==========================================

print("\nSummary Statistics:\n", df.describe())

print("\nSkewness:\n", df.skew(numeric_only=True))

numerical_cols = df.select_dtypes(include=np.number).columns
categorical_cols = df.select_dtypes(include="object").columns

print("\nNumerical Columns:", list(numerical_cols))
print("Categorical Columns:", list(categorical_cols))

# ==========================================
# DATA CLEANING
# ==========================================

print("\nMissing Values:\n", df.isnull().sum())

print("Duplicate rows:", df.duplicated().sum())
df.drop_duplicates(inplace=True)

df["churn"] = df["churn"].astype(int)

# ==========================================
# UNIVARIATE ANALYSIS
# ==========================================

print("\nGenerating Univariate Plots...")

plt.figure()
sns.histplot(df["annual_income"], kde=True)
plt.title("Income Distribution")
plt.savefig("income_distribution.png")
plt.close()

plt.figure()
sns.histplot(df["spending_score"], kde=True)
plt.title("Spending Score Distribution")
plt.savefig("spending_distribution.png")
plt.close()

plt.figure()
sns.countplot(x="city", data=df)
plt.xticks(rotation=45)
plt.title("Customers by City")
plt.savefig("city_count.png")
plt.close()

plt.figure()
df["preferred_category"].value_counts().plot.pie(autopct="%1.1f%%")
plt.title("Category Distribution")
plt.ylabel("")
plt.savefig("category_pie.png")
plt.close()

# ==========================================
# BIVARIATE ANALYSIS
# ==========================================

print("\nGenerating Bivariate Analysis...")

plt.figure()
sns.regplot(x="annual_income", y="spending_score", data=df)
plt.title("Income vs Spending")
plt.savefig("income_vs_spending.png")
plt.close()

plt.figure()
sns.boxplot(x="gender", y="spending_score", data=df)
plt.title("Gender vs Spending")
plt.savefig("gender_spending.png")
plt.close()

crosstab = pd.crosstab(df["preferred_category"], df["churn"])
crosstab.plot(kind="bar", stacked=True)
plt.title("Category vs Churn")
plt.savefig("category_churn.png")
plt.close()

plt.figure(figsize=(10,8))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.savefig("correlation_heatmap.png")
plt.close()

# ==========================================
# OUTLIER DETECTION
# ==========================================

print("\nDetecting Outliers...")

Q1 = df["avg_order_value"].quantile(0.25)
Q3 = df["avg_order_value"].quantile(0.75)
IQR = Q3 - Q1

outliers = df[(df["avg_order_value"] < Q1 - 1.5*IQR) |
              (df["avg_order_value"] > Q3 + 1.5*IQR)]

print("AOV Outliers:", len(outliers))

z_scores = np.abs(stats.zscore(df["annual_income"]))
income_outliers = df[z_scores > 3]
print("Income Outliers:", len(income_outliers))

# ==========================================
# FEATURE ENGINEERING
# ==========================================

print("\nCreating Business Features...")

df["CLV"] = df["total_orders"] * df["avg_order_value"]

df["income_group"] = pd.cut(
    df["annual_income"],
    bins=[0,40000,80000,200000],
    labels=["Low","Medium","High"]
)

df["order_frequency"] = df["total_orders"] / df["membership_years"]

df["Recency"] = df["last_purchase_days"]
df["Frequency"] = df["total_orders"]
df["Monetary"] = df["CLV"]

# ==========================================
# ADVANCED ANALYSIS
# ==========================================

print("\nTop 10 Customers by CLV:")
print(df.sort_values("CLV", ascending=False)[
    ["customer_id","CLV"]
].head(10))

print("\nRevenue by City:")
city_revenue = df.groupby("city")["CLV"].sum().sort_values(ascending=False)
print(city_revenue)

print("\nMost Profitable Category:")
print(df.groupby("preferred_category")["CLV"].sum().sort_values(ascending=False))

print("\nChurn Rate:", round(df["churn"].mean()*100,2), "%")

print("\nIncome vs Spending Correlation:",
      round(df["annual_income"].corr(df["spending_score"]),3))

# ==========================================
# ML PREPARATION
# ==========================================

print("\nPreparing Data for Machine Learning...")

df_ml = pd.get_dummies(df, drop_first=True)

scaler = StandardScaler()
num_cols = df_ml.select_dtypes(include=np.number).columns
df_ml[num_cols] = scaler.fit_transform(df_ml[num_cols])

print("Final ML Dataset Shape:", df_ml.shape)

print("\nEDA Completed Successfully!")