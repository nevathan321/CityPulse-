import pandas as pd


df = pd.read_csv(r"Pyt\SR2025.csv", on_bad_lines='skip', encoding='latin1')

df_cleaned = df[df['Status'].str.strip().str.lower() != 'completed']

df_cleaned.to_csv(r"Pyt\SR2025_cleaned.csv", index=False)



print(df_cleaned.to_string)




