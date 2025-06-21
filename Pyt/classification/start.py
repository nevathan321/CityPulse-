import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

df = pd.read_csv("Pyt\data\SR2025_cleaned.csv", encoding="latin1")
df.columns = df.columns.str.strip()  # Clean column names
df = df.dropna(subset=['Status', 'Service Request Type'])  # Drop key nulls
def breaker():
    print('-'*100)

print(df['Status'].value_counts()) # gives counts of all status categories
breaker()
print(df['Service Request Type'].value_counts()) # displays counts of all service request types
breaker()
print(df.info())
breaker()
print(df.describe())

df['Creation Date'] = pd.to_datetime(df['Creation Date'])
df['Month'] = df['Creation Date'].dt.month
df['Weekday'] = df['Creation Date'].dt.dayofweek
df['Hour'] = df['Creation Date'].dt.hour

#df['Intersection'] = df['Intersection Street 1'].fillna('') + ' & ' + df['Intersection Street 2'].fillna('')

#df['Intersection'] = df['Intersection'].str.lower().str.strip()
print(df['First 3 Chars of Postal Code'].unique())
def smart_location(row):
    pc = str(row['First 3 Chars of Postal Code']).strip().lower()
    s1 = row['Intersection Street 1']
    s2 = row['Intersection Street 2']
    ward = str(row['Ward']).strip().lower() if 'Ward' in row and pd.notna(row['Ward']) else None

    if pc == "intersection":
        # Real intersection case
        if pd.notna(s1) and pd.notna(s2) and s1.strip() != '' and s2.strip() != '':
            return f"{s1.lower().strip()} & {s2.lower().strip()}"
        elif pd.notna(s1) and s1.strip() != '':
            return s1.lower().strip()
        elif pd.notna(s2) and s2.strip() != '':
            return s2.lower().strip()
        else:
            return "unknown"
    else:
        # No intersection, so return ward or postal code
        if ward and ward != "":
            return ward
        elif pc != "":
            return pc
        else:
            return "unknown"

df['Intersection'] = df.apply(smart_location, axis=1)
top_10 = df['Intersection'].value_counts().head(20)
print(top_10)






