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

import seaborn as sns
import matplotlib.pyplot as plt


week_days = {}

with open(r"Pyt\visualizations\daysData.txt","r") as f:
    for line in f:
        comb = line.strip().split(" ")
        week_days[comb[0]] = int(comb[1])

x = list(week_days.keys())
y = list(week_days.values())

plt.plot(x, y, marker='o')  # Add marker for each point
plt.title("Daily Data")
plt.xlabel("Day")
plt.ylabel("Value")
plt.grid(True)
plt.show()
