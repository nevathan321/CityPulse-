#  Completed vs Cancelled vs unknown requests

import pandas as pd
import matplotlib.pyplot as plt

# Load your CSV
df = pd.read_csv("Pyt\data\SR2025.csv", encoding="latin1",on_bad_lines='skip')

# Count each status
status_counts = df['Status'].value_counts()

# Plot a bar chart
status_counts.plot(kind='bar', color=['green', 'red', 'gray', 'orange'])

# Add labels and title
plt.xlabel('Status')
plt.ylabel('Count')
plt.title('Distribution of Status Types')
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()
