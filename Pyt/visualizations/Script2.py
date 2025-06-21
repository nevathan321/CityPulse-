import pandas as pd

# Load the data
df = pd.read_csv("data/raw/SR2025.csv", encoding="latin1", on_bad_lines='skip')

# Create a dictionary for replacements
replacements = {
    "Waste or Illegal Dumping on Private Property": "Illegal Dumping on Private Property",
    "Long Grass and Prohibited Plants on Private Property": "Unlawful Grass/Plants on Private Property",
    "Waste Set Out - Wrong Location / Time/ Day": "Incorrect Waste Set Out (Location/day/time)",
    "Residential: Bin: Wrong Delivery or Bin Return": "Wrong Residential Bin Delivery",
    "Missing / Damaged Street or Traffic Sign": "Faulty Traffic Sign",
    "Property Standards and Maintenance Violations": "Property Maintenance Violations"
}

# Clean up whitespaces and replace values
df["Service Request Type"] = df["Service Request Type"].str.strip().replace(replacements)

# Save the updated DataFrame
df.to_csv("Pyt/data/SR2025.csv", index=False)

print("DONE")