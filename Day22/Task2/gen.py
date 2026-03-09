# ==========================================
# E-COMMERCE DATA ANALYSIS PROJECT
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# ==========================================
# PART 0 – GENERATE DATASET
# ==========================================

n = 2000

order_ids = np.arange(10001, 10001+n)
customer_ids = np.random.randint(1000, 2000, n)

categories = np.random.choice(
    ['Technology', 'Furniture', 'Office Supplies'], n)

regions = np.random.choice(
    ['East', 'West', 'Central', 'South'], n)

sales = np.random.gamma(4, 100, n).round(2)
quantity = np.random.randint(1, 10, n)

discount = np.random.choice(
    [0, 0.05, 0.1, 0.15, 0.2, 0.3],
    n,
    p=[0.4, 0.15, 0.15, 0.1, 0.1, 0.1]
)

profit = (sales*(1-discount)*np.random.uniform(0.05,0.3,n) -
          sales*discount*np.random.uniform(0.5,1.2,n)).round(2)

order_dates = pd.date_range(start='2022-01-01', periods=n, freq='D')

df = pd.DataFrame({
    'Order ID': order_ids,
    'Customer ID': customer_ids,
    'Category': categories,
    'Sales': sales,
    'Quantity': quantity,
    'Discount': discount,
    'Profit': profit,
    'Order Date': np.random.choice(order_dates, n),
    'Region': regions
})

df.to_csv("ecommerce_sales.csv", index=False)

print("\nDataset Generated Successfully!\n")

# ==========================================
# PART 1 – DATA PREPARATION
# ==========================================

print("First 10 Rows:")
print(df.head(10))

print("\nDataset Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

df['Order Date'] = pd.to_datetime(df['Order Date'])
df = df.drop_duplicates()
df['Revenue'] = df['Sales'] - df['Discount']

# ==========================================
# PART 2 – DESCRIPTIVE STATISTICS
# ==========================================

print("\n--- CENTRAL TENDENCY ---")
print("Sales Mean:", df['Sales'].mean())
print("Sales Median:", df['Sales'].median())
print("Sales Mode:", df['Sales'].mode()[0])
print("Profit Mean:", df['Profit'].mean())
print("Profit Median:", df['Profit'].median())

print("\n--- DISPERSION ---")
print("Sales Range:", df['Sales'].max() - df['Sales'].min())
print("Profit Variance:", df['Profit'].var())
print("Profit Std Dev:", df['Profit'].std())

Q1 = df['Sales'].quantile(0.25)
Q3 = df['Sales'].quantile(0.75)
print("Sales IQR:", Q3 - Q1)

print("\n--- SHAPE ---")
print("Sales Skewness:", df['Sales'].skew())
print("Sales Kurtosis:", df['Sales'].kurt())

# Group Analysis
print("\nAverage Sales by Region:")
print(df.groupby('Region')['Sales'].mean())

print("\nAverage Profit by Category:")
print(df.groupby('Category')['Profit'].mean())

df['Month'] = df['Order Date'].dt.to_period('M')
monthly_sales = df.groupby('Month')['Sales'].sum()

# ==========================================
# PART 3 – VISUALIZATION
# ==========================================

# Line Plot
monthly_sales.plot()
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.grid(True)
plt.show()

# Bar Charts
df.groupby('Region')['Sales'].sum().plot(kind='bar')
plt.title("Sales by Region")
plt.grid(True)
plt.show()

df.groupby('Category')['Profit'].sum().plot(kind='bar')
plt.title("Profit by Category")
plt.grid(True)
plt.show()

# Histograms
plt.hist(df['Sales'], bins=30)
plt.title("Sales Distribution")
plt.grid(True)
plt.show()

plt.hist(df['Profit'], bins=30)
plt.title("Profit Distribution")
plt.grid(True)
plt.show()

# Boxplot
df.boxplot(column='Sales', by='Category')
plt.title("Sales by Category")
plt.suptitle("")
plt.grid(True)
plt.show()

# Scatter
plt.scatter(df['Sales'], df['Profit'])
plt.title("Sales vs Profit")
plt.xlabel("Sales")
plt.ylabel("Profit")
plt.grid(True)
plt.show()

plt.scatter(df['Discount'], df['Profit'])
plt.title("Discount vs Profit")
plt.xlabel("Discount")
plt.ylabel("Profit")
plt.grid(True)
plt.show()

# ==========================================
# PART 4 – COVARIANCE & CORRELATION
# ==========================================

print("\nCovariance Matrix:")
print(df[['Sales','Profit','Discount','Quantity']].cov())

print("\nCorrelation Matrix:")
print(df[['Sales','Profit','Discount','Quantity']].corr())

# ==========================================
# PART 5 – PROBABILITY
# ==========================================

avg_sales = df['Sales'].mean()

print("\n--- PROBABILITY ---")
print("P(Sales > Avg):", np.mean(df['Sales'] > avg_sales))
print("P(Profit < 0):", np.mean(df['Profit'] < 0))
print("P(Region = West):", np.mean(df['Region'] == 'West'))

print("\nConditional Probability:")
print("P(Neg Profit | Discount > 20%):",
      np.mean(df[df['Discount'] > 0.2]['Profit'] < 0))

print("P(High Sales | Technology):",
      np.mean(df[df['Category']=='Technology']['Sales'] > avg_sales))

# Binomial Simulation
p = np.mean(df['Profit'] > 0)
simulation = np.random.binomial(1, p, 1000)

print("\nSimulated Profitable Rate:", simulation.mean())
print("Actual Profitable Rate:", p)

# ==========================================
# PART 6 – LAW OF LARGE NUMBERS
# ==========================================

profits = np.random.choice(df['Profit'], 5000)
running_mean = np.cumsum(profits) / np.arange(1,5001)

plt.plot(running_mean)
plt.axhline(df['Profit'].mean())
plt.title("Law of Large Numbers")
plt.grid(True)
plt.show()

# ==========================================
# PART 7 – EXPECTED VALUE & VARIANCE
# ==========================================

print("\nExpected Sales:", df['Sales'].mean())
print("Variance of Profit:", df['Profit'].var())

# ==========================================
# FINAL MESSAGE
# ==========================================

print("\nPROJECT COMPLETED SUCCESSFULLY!")