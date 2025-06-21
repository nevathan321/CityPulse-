import pandas as pd

df = pd.read_csv("Pyt/data/SR2025.csv", encoding="latin1", on_bad_lines='skip')

print("STARTING")

for index, service in enumerate(df["Service Request Type"]):
    if pd.isna(service):
        continue

    service = str(service).strip()
    print(f"DEBUG: {repr(service)}")

    if service == "'Waste or Illegal Dumping on Private Property'":
        print("DETECTED")
        df.at[index, "Service Request Type"] = "Illegal Dumping on Private Property"
    elif service == "Long Grass and Prohibited Plants on Private Property":
        print("DETECTED")
        df.at[index, "Service Request Type"] = "Unlawful Grass/Plants on Private Property"
    elif service == "Waste Set Out - Wrong Location / Time/ Day":
        print("DETECTED")
        df.at[index, "Service Request Type"] = "Incorrect Waste Set Out (Location/day/time)"
    elif service == "Residential: Bin: Wrong Delivery or Bin Return":
        print("DETECTED")
        df.at[index, "Service Request Type"] = "Wrong Residential Bin Delivery"
    elif service == "Missing / Damaged Street or Traffic Sign":
        print("DETECTED")
        df.at[index, "Service Request Type"] = "Faulty Traffic Sign"
    elif service == "Property Standards and Maintenance Violations":
        print("DETECTED")
        df.at[index, "Service Request Type"] = "Property Maintenance Violations"

df.to_csv("Pyt/data/SR2025.csv", index=False)
print("FINALLY DONE")
