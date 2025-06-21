import pandas as pd

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

df = pd.get_dummies(df, columns=['Service Request Type', 'Neighbourhood', 'Service Channel'], drop_first=True)






