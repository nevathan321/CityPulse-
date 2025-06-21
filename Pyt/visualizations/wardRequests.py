import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


df = pd.read_csv("Pyt\data\SR2025.csv", encoding="latin1",on_bad_lines='skip')
ward_counts = df['Ward'].dropna().value_counts().sort_values(ascending=False)


plt.figure(figsize=(12, 8))
sns.barplot(x=ward_counts.values, y=ward_counts.index, palette="magma")
plt.title("Number of Service Requests by Ward")
plt.xlabel("Number of Requests")
plt.ylabel("Ward")
plt.tight_layout()
plt.show()
