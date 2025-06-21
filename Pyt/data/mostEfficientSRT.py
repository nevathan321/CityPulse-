import pandas as pd

# Load data
df = pd.read_csv("Pyt/data/SR2025.csv", encoding="latin1", on_bad_lines='skip')

# Initialize dictionary to track each Service Request Type
sr_types = {}

# Iterate through the rows
for index, row in df.iterrows():
    sr_type = row["Service Request Type"]
    status = row["Status"]

    if sr_type not in sr_types:
        sr_types[sr_type] = {"Cases": 0, "Completed": 0}

    sr_types[sr_type]["Cases"] += 1
    if status == "Completed":
        sr_types[sr_type]["Completed"] += 1

# Calculate efficiency and find most efficient SR Type
most_efficient_type = None
highest_efficiency = -1

for sr_type, stats in sr_types.items():
    cases = stats["Cases"]
    completed = stats["Completed"]

    if cases > 0:
        efficiency = completed / cases
        sr_types[sr_type]["Efficiency"] = efficiency

        if efficiency > highest_efficiency:
            highest_efficiency = efficiency
            most_efficient_type = sr_type
    else:
        sr_types[sr_type]["Efficiency"] = None

# Print result
print(f"Most efficient SR Type: {most_efficient_type} with {highest_efficiency:.2%} efficiency")
