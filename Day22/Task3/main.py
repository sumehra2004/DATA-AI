# =====================================
# LOAN APPROVAL ANALYSIS PROJECT
# =====================================

# 1️⃣ Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 2️⃣ Load Dataset
df = pd.read_csv("loan_prediction_dataset.csv")

print("\nFirst 5 Rows:\n")
print(df.head())

print("\nDataset Info:\n")
print(df.info())

print("\nMissing Values:\n")
print(df.isnull().sum())

# 3️⃣ Basic Statistics
print("\nDescriptive Statistics:\n")
print(df.describe())

# 4️⃣ Approval Rate
approval_rate = df['loan_approved'].mean()
print("\nOverall Loan Approval Rate:", approval_rate)

# 5️⃣ Group Analysis

print("\nApproval Rate by Home Ownership:")
print(df.groupby('home_owner')['loan_approved'].mean())

print("\nApproval Rate by Dependents:")
print(df.groupby('dependents')['loan_approved'].mean())

# 6️⃣ Visualization

# Age Distribution
plt.figure()
plt.hist(df['age'], bins=20)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.show()

# Income Distribution
plt.figure()
plt.hist(df['income'], bins=30)
plt.title("Income Distribution")
plt.xlabel("Income")
plt.ylabel("Frequency")
plt.show()

# Credit Score Distribution
plt.figure()
plt.hist(df['credit_score'], bins=30)
plt.title("Credit Score Distribution")
plt.xlabel("Credit Score")
plt.ylabel("Frequency")
plt.show()

# Income vs Credit Score
plt.figure()
plt.scatter(df['income'], df['credit_score'])
plt.title("Income vs Credit Score")
plt.xlabel("Income")
plt.ylabel("Credit Score")
plt.show()

# Approval by Home Owner
plt.figure()
df.groupby('home_owner')['loan_approved'].consider = df.groupby('home_owner')['loan_approved'].mean()
df.groupby('home_owner')['loan_approved'].mean().plot(kind='bar')
plt.title("Loan Approval by Home Ownership")
plt.xlabel("Home Owner (0=No, 1=Yes)")
plt.ylabel("Approval Rate")
plt.show()

# 7️⃣ Correlation Matrix
print("\nCorrelation Matrix:\n")
print(df.corr())

# 8️⃣ Probability Calculations
total = len(df)

p_approved = df['loan_approved'].sum() / total
p_high_credit = len(df[df['credit_score'] > 700]) / total
p_home_owner = len(df[df['home_owner'] == 1]) / total

print("\nProbability Loan Approved:", p_approved)
print("Probability Credit Score > 700:", p_high_credit)
print("Probability Home Owner:", p_home_owner)

# Conditional Probability
p_approved_high_credit = len(df[(df['loan_approved']==1) & (df['credit_score']>700)]) / len(df[df['credit_score']>700])
print("\nP(Approved | Credit Score > 700):", p_approved_high_credit)

# 9️⃣ Expected Value (Risk)
expected_income = df['income'].mean()
variance_income = df['income'].var()

print("\nExpected Income:", expected_income)
print("Income Variance:", variance_income)

print("\nProject Completed Successfully!")# =====================================
# LOAN APPROVAL ANALYSIS PROJECT
# =====================================

# 1️⃣ Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 2️⃣ Load Dataset
df = pd.read_csv("loan_prediction_dataset.csv")

print("\nFirst 5 Rows:\n")
print(df.head())

print("\nDataset Info:\n")
print(df.info())

print("\nMissing Values:\n")
print(df.isnull().sum())

# 3️⃣ Basic Statistics
print("\nDescriptive Statistics:\n")
print(df.describe())

# 4️⃣ Approval Rate
approval_rate = df['loan_approved'].mean()
print("\nOverall Loan Approval Rate:", approval_rate)

# 5️⃣ Group Analysis

print("\nApproval Rate by Home Ownership:")
print(df.groupby('home_owner')['loan_approved'].mean())

print("\nApproval Rate by Dependents:")
print(df.groupby('dependents')['loan_approved'].mean())

# 6️⃣ Visualization

# Age Distribution
plt.figure()
plt.hist(df['age'], bins=20)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.show()

# Income Distribution
plt.figure()
plt.hist(df['income'], bins=30)
plt.title("Income Distribution")
plt.xlabel("Income")
plt.ylabel("Frequency")
plt.show()

# Credit Score Distribution
plt.figure()
plt.hist(df['credit_score'], bins=30)
plt.title("Credit Score Distribution")
plt.xlabel("Credit Score")
plt.ylabel("Frequency")
plt.show()

# Income vs Credit Score
plt.figure()
plt.scatter(df['income'], df['credit_score'])
plt.title("Income vs Credit Score")
plt.xlabel("Income")
plt.ylabel("Credit Score")
plt.show()

# Approval by Home Owner
plt.figure()
df.groupby('home_owner')['loan_approved'].consider = df.groupby('home_owner')['loan_approved'].mean()
df.groupby('home_owner')['loan_approved'].mean().plot(kind='bar')
plt.title("Loan Approval by Home Ownership")
plt.xlabel("Home Owner (0=No, 1=Yes)")
plt.ylabel("Approval Rate")
plt.show()

# 7️⃣ Correlation Matrix
print("\nCorrelation Matrix:\n")
print(df.corr())

# 8️⃣ Probability Calculations
total = len(df)

p_approved = df['loan_approved'].sum() / total
p_high_credit = len(df[df['credit_score'] > 700]) / total
p_home_owner = len(df[df['home_owner'] == 1]) / total

print("\nProbability Loan Approved:", p_approved)
print("Probability Credit Score > 700:", p_high_credit)
print("Probability Home Owner:", p_home_owner)

# Conditional Probability
p_approved_high_credit = len(df[(df['loan_approved']==1) & (df['credit_score']>700)]) / len(df[df['credit_score']>700])
print("\nP(Approved | Credit Score > 700):", p_approved_high_credit)

# 9️⃣ Expected Value (Risk)
expected_income = df['income'].mean()
variance_income = df['income'].var()

print("\nExpected Income:", expected_income)
print("Income Variance:", variance_income)

print("\nProject Completed Successfully!")