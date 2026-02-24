import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Load dataset
tips = sns.load_dataset("tips")

# -----------------------------
# DESCRIPTIVE STATISTICS
# -----------------------------
print("\nSummary Statistics:")
print(tips.describe())

print("\nMean Total Bill:", tips['total_bill'].mean())
print("Median Total Bill:", tips['total_bill'].median())
print("Standard Deviation:", tips['total_bill'].std())

# -----------------------------
# VISUALIZATIONS
# -----------------------------
plt.hist(tips['total_bill'], bins=20)
plt.xlabel("Total Bill")
plt.ylabel("Frequency")
plt.title("Distribution of Total Bill")
plt.show()

sns.boxplot(x=tips['total_bill'])
plt.title("Boxplot of Total Bill")
plt.show()

# -----------------------------
# EMPIRICAL PROBABILITY
# -----------------------------
prob_empirical = np.mean(tips['total_bill'] > 30)
print("\nEmpirical Probability (bill > $30):", prob_empirical)

# -----------------------------
# MONTE CARLO SIMULATION
# -----------------------------
sample = np.random.choice(tips['total_bill'], size=10000, replace=True)
prob_simulated = np.mean(sample > 30)
print("Simulated Probability:", prob_simulated)

# -----------------------------
# NORMAL APPROXIMATION
# -----------------------------
mean = tips['total_bill'].mean()
std = tips['total_bill'].std()

prob_normal = 1 - norm.cdf(30, mean, std)
print("Normal Approximation Probability:", prob_normal)