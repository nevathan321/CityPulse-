# visualize avg number of service requests per day
# Top service request types
#  Requests by ward
# Requests by division
#  Completed vs Cancelled vs unknown requests
# Request patterns by hours
#Total service request
# Completion rate
#Most active ward
# Most service type

import pandas as pd
import seaborn as sns
from datetime import datetime


df = pd.read_csv("Pyt\data\SR2025.csv", encoding="latin1",on_bad_lines='skip')

#print(df["Creation Date"][3])

#date = (df["Creation Date"][3].strip())[0:10].strip()
#date_obj = datetime.strptime(date, "%Y-%m-%d")
#day_of_week = date_obj.strftime("%A")
#print(day_of_week)

week_days = {"Sunday":0, "Monday":0,"Tuesday":0,"Wednesday":0,"Thursday":0,"Friday":0,"Saturday":0,}

def get_day(Creation_Date):
    date = (Creation_Date.strip())[0:10].strip()
    date_obj = datetime.strptime(date,"%Y-%m-%d")
    day_of_week = date_obj.strftime("%A")
    return day_of_week

for dates in df["Creation Date"]:
    week_days[get_day(dates)] += 1
    print("DOING")

with open("daysData.txt",'w') as f:
    for day in week_days:
        f.write(f"{day} {week_days.get(day)}" + "\n")
        
    f.close()








    




