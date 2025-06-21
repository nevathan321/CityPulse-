import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("Pyt\data\SR2025.csv", encoding="latin1",on_bad_lines='skip')

status_counts = df['Status'].value_counts()


status_counts.plot(kind='bar', color=['green', 'red', 'gray', 'orange'])


plt.xlabel('Status')
plt.ylabel('Count')
plt.title('Distribution of Status Types')
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
