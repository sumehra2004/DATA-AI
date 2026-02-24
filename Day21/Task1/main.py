# ==========================================
# NETFLIX COMPLETE NUMPY + PANDAS PROJECT
# ==========================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ==============================
# CONFIGURATION
# ==============================

CSV_PATH = "netflix_titles.csv"   # Keep file in same folder

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError("Place netflix_titles.csv in the same folder as this script.")

# ==============================
# PART 1 — NUMPY TASKS
# ==============================

print("===== NUMPY TASKS =====")

# 1. Create NumPy array
arr = np.array([10,20,30,40,50,60,70,80,90,100])
print("Array:", arr)
print("Shape:", arr.shape)
print("Size:", arr.size)
print("Data Type:", arr.dtype)

# 2. Arithmetic operations
print("Addition:", arr + 5)
print("Subtraction:", arr - 5)
print("Multiplication:", arr * 2)
print("Division:", arr / 2)

# 3. 2D Array
arr2d = np.array([[1,2,3],[4,5,6],[7,8,9]])
print("Specific element:", arr2d[0,1])
print("Last element:", arr2d[2,2])

# 4. Slicing
print("Slice:", arr[2:7])

# 5. Reshape
reshaped = arr.reshape(5,2)
print("Reshaped:\n", reshaped)

# 6. Broadcasting
matrix = np.array([[1,2,3],[4,5,6]])
print("Broadcasting:\n", matrix + 10)


# ==============================
# PART 2 — PANDAS TASKS
# ==============================

print("\n===== PANDAS TASKS =====")

# 7. Load dataset
df = pd.read_csv(CSV_PATH)

# 8. First & Last rows
print(df.head(10))
print(df.tail(10))

# 9. Info & columns
print("\nDataset Info:")
print(df.info())
print("Columns:", df.columns)

# 10. Missing values
print("\nMissing Values:\n", df.isnull().sum())
df.fillna("Unknown", inplace=True)

# 11. Select specific columns
print(df[['title','type','release_year']].head())

# 12. Filter rows
movies_2020 = df[(df['type']=='Movie') & (df['release_year']==2020)]
print("Movies in 2020:", movies_2020.shape)

# 13. Add new column
df['is_recent'] = df['release_year'] >= 2018

# 14. Remove column
if 'description' in df.columns:
    df.drop('description', axis=1, inplace=True)

# 15. Rename column
df.rename(columns={'release_year':'year'}, inplace=True)

# 16. Sort data
df_sorted = df.sort_values(by='year', ascending=False)

# 17. Indexing & slicing
print(df.iloc[0:5])
print(df.loc[df['year']>2015].head())

# 18. GroupBy
print("GroupBy type:\n", df.groupby('type')['title'].count())

# 19. Pivot Table
pivot = pd.pivot_table(df,
                       values='title',
                       index='year',
                       columns='type',
                       aggfunc='count')
print(pivot.head())

# 20. shift()
df['previous_year'] = df['year'].shift(1)
print(df[['year','previous_year']].head())

# 21. rank()
df['rank_year'] = df['year'].rank()
print(df[['year','rank_year']].head())

# 22. rolling()
df['rolling_avg'] = df['year'].rolling(5).mean()
print(df[['year','rolling_avg']].head())


# ==============================
# PART 3 — VISUALIZATION
# ==============================

print("\n===== VISUALIZATION =====")

# 23. Bar chart
plt.figure()
df['type'].value_counts().plot(kind='bar')
plt.title("Movies vs TV Shows")
plt.xlabel("Type")
plt.ylabel("Count")
plt.savefig("bar_chart.png")
plt.show()

# 24. Pie chart
plt.figure()
df['type'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title("Content Distribution")
plt.ylabel("")
plt.savefig("pie_chart.png")
plt.show()

# 25. Histogram
plt.figure()
plt.hist(df['year'], bins=20)
plt.title("Release Year Distribution")
plt.xlabel("Year")
plt.ylabel("Count")
plt.savefig("histogram.png")
plt.show()

# 26. Subplots
fig, ax = plt.subplots(1,2, figsize=(12,4))

df['type'].value_counts().plot(kind='bar', ax=ax[0])
ax[0].set_title("Movies vs TV Shows")

ax[1].hist(df['year'], bins=20)
ax[1].set_title("Year Distribution")

plt.savefig("subplots.png")
plt.show()


# ==============================
# ANALYSIS TASKS
# ==============================

print("\n===== ANALYSIS =====")

# 29. Count Movies & TV Shows
print("Movies & TV Shows:\n", df['type'].value_counts())

# 30. Most common release year
print("Most Common Year:", df['year'].mode())

# 31. Trend chart
plt.figure()
df.groupby('year')['title'].count().plot()
plt.title("Content Trend Over Years")
plt.xlabel("Year")
plt.ylabel("Number of Titles")
plt.savefig("trend.png")
plt.show()

# 34. NumPy + Pandas together
print("Mean Year:", np.mean(df['year']))
print("Standard Deviation:", np.std(df['year']))

# 35. Statistical analysis
print("Statistics:\n", df['year'].describe())

# 37. Save results
df.to_csv("netflix_analysis_output.csv", index=False)

print("\nAnalysis Completed Successfully!")