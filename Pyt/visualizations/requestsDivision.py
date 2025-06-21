# Requests by division
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Pyt\data\SR2025.csv", encoding="latin1",on_bad_lines='skip')
# Count service requests by division (drop missing if needed)
division_counts = df['Division'].dropna().value_counts().sort_values(ascending=False)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(x=division_counts.values, y=division_counts.index, palette="coolwarm")
plt.title("Number of Service Requests by Division")
plt.xlabel("Number of Requests")
plt.ylabel("Division")
plt.tight_layout()
plt.show()
