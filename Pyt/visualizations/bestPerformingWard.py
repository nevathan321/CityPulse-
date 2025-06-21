import pandas as pd

df = pd.read_csv("Pyt\data\SR2025.csv", encoding="latin1",on_bad_lines='skip')

df = pd.read_csv("Pyt\data\SR2025.csv", encoding="latin1",on_bad_lines='skip')
ward_counts = df['Ward'].dropna().value_counts().sort_values(ascending=False)

print(ward_counts)
for x in ward_counts:
    print(x)
"""
wards = {}

print(df["Ward"].unique())

for y in range(3):
    for x in df["Ward"].unique():
        print(x)
        wards[x["count"]] = 0
        wards[x["completion"]] = 0

print(wards)
"""

"""
print(df["Status"][2])


for ward,index in enumerate(df["Ward"]):
    if df["Status"][index] == 'Completed':
        wards[ward] += 1

"""