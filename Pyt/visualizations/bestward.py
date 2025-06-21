import pandas as pd

wards = {}

df = pd.read_csv("Pyt/data/SR2025.csv", encoding="latin1", on_bad_lines='skip')

for index, row in df.iterrows():
    ward = row["Service Request Type"]
    status = row["Status"]

    if ward not in wards:
        if ward == "Fireworks":
            continue
        wards[ward] = {"Cases": 0, "Completed": 0}

    wards[ward]["Cases"] += 1
    if status == "Completed":
        wards[ward]["Completed"] += 1

# Calculate efficiencies
most_efficient_ward = None
highest_efficiency = -1

for ward, stats in wards.items():
    cases = stats["Cases"]
    completed = stats["Completed"]
    
    if cases > 0:
        efficiency = completed / cases
        stats["Efficiency"] = efficiency
        if efficiency > highest_efficiency:
            highest_efficiency = efficiency
            most_efficient_ward = ward
    else:
        stats["Efficiency"] = None

print(f"Most efficient ward: {most_efficient_ward} with {highest_efficiency:.2%} efficiency")