import pandas as pd
import matplotlib.pyplot as plt

from constants import Teams

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 1000)

frame = pd.read_csv('role_stat_breakdown.csv')
points = pd.read_csv('season_points.csv')
frame = frame.merge(points, on='team')




print(frame)

plt.figure(figsize=(10, 8))

plt.title('League Points vs DPS Damage %')
for ind in frame.index:
    row = frame.loc[ind, :]
    label = row['team']
    x = row['dps_dmg']
    y = row['points']
    team = row['team']
    color = Teams.TeamColors[team]
    plt.scatter(x, y, label=label, color=color)


for ind in frame.index:
    row = frame.loc[ind, :]
    label = row['team']
    x = row['dps_dmg']
    y = row['points']
    team = row['team']
    color = Teams.TeamColors[team]
    plt.text(x*1.0001, y*1.0001, label, color=color, weight='bold')


plt.xlabel('DPS Damage %')
plt.ylabel('League Points')
plt.show()
