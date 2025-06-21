import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Pyt\data\SR2025.csv", encoding="latin1",on_bad_lines='skip')
top_20 = df['Service Request Type'].value_counts().head(20)

top_20_requests = df['Service Request Type'].value_counts().head(20)


plt.figure(figsize=(12, 8))
sns.barplot(x=top_20_requests.values, y=top_20_requests.index, palette="viridis")
plt.title("Top 20 Most Common Service Request Types")
plt.xlabel("Number of Requests")
plt.ylabel("Service Request Type")
plt.tight_layout()
plt.show()

