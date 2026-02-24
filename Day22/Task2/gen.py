import pandas as pd
import numpy as np

np.random.seed(42)

# Number of orders
n = 2000

# Generate data
order_ids = np.arange(10001, 10001+n)
customer_ids = np.random.randint(1000, 2000, n)

categories = np.random.choice(
    ['Technology', 'Furniture', 'Office Supplies'],
    n
)

regions = np.random.choice(
    ['East', 'West', 'Central', 'South'],
    n
)

sales = np.random.gamma(shape=4, scale=100, size=n).round(2)

quantity = np.random.randint(1, 10, n)

discount = np.random.choice(
    [0, 0.05, 0.1, 0.15, 0.2, 0.3],
    n,
    p=[0.4, 0.15, 0.15, 0.1, 0.1, 0.1]
)

profit = (sales * (1 - discount) * np.random.uniform(0.05, 0.3, n) - 
          sales * discount * np.random.uniform(0.5, 1.2, n)).round(2)

order_dates = pd.date_range(
    start='2022-01-01',
    periods=n,
    freq='D'
)

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

print("Dataset generated successfully!")
print(df.head())