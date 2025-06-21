# Request patterns by hours
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("Pyt\data\SR2025.csv", encoding="latin1",on_bad_lines='skip')

hours = {"00:00": 0, "01:00": 0,"02:00": 0,"03:00": 0,"04:00": 0,"05:00": 0,"06:00": 0,"07:00": 0,"08:00": 0,"09:00": 0,"10:00": 0,"11:00": 0,"12:00": 0,"13:00": 0,"14:00": 0,"15:00": 0,"16:00": 0,"17:00": 0,"18:00": 0,"19:00": 0,"20:00": 0,"21:00": 0,"22:00": 0,"23:00": 0}

def get_hour(Creation_date):
    hour = Creation_date[11:13]
    string = f"{hour}:00"
    hours[string] +=1

for x in df["Creation Date"]:
    get_hour(x)


x = list(hours.keys())
y = list(hours.values())

plt.plot(x, y, marker='o')  # Add marker for each point
plt.title("Hourly Data")
plt.xlabel("Hours")
plt.ylabel("Requests")
plt.grid(True)
plt.show()
    
