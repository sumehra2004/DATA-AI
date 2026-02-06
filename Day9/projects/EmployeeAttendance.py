import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("Attendance.csv")
print("Average Days Present:", df["Days_Present"].mean())
print(df)
plt.bar(df["Employee"], df["Days_Present"])
plt.xlabel("Employee")
plt.ylabel("Days Present")
plt.title("Employee Attendance")

