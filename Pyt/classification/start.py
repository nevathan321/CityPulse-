import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder


df = pd.read_csv("Pyt\\data\\SR2025.csv", encoding="latin1", on_bad_lines="skip")
df.columns = df.columns.str.strip()  # Clean column names


df = df.dropna(subset=['Status', 'Service Request Type', 'Division', 'Ward'])


le_status = LabelEncoder()
df['Status_encoded'] = le_status.fit_transform(df['Status'])


cols_to_encode = ['Service Request Type', 'Division', 'Ward']
for col in cols_to_encode:
    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found in DataFrame!")


df_encoded = pd.get_dummies(df[cols_to_encode], drop_first=True)


df['Month'] = pd.to_datetime(df['Creation Date'], errors='coerce').dt.month
df['Weekday'] = pd.to_datetime(df['Creation Date'], errors='coerce').dt.dayofweek
df['Hour'] = pd.to_datetime(df['Creation Date'], errors='coerce').dt.hour
numeric_features = df[['Month', 'Weekday', 'Hour']]


X = pd.concat([df_encoded, numeric_features], axis=1)
y = df['Status_encoded']


assert X.select_dtypes(include='object').empty, "Non-numeric columns still in X!"


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=101
)


clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)


y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred, target_names=le_status.classes_))
