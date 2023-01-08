import pandas as pd
import matplotlib.pyplot as plt

from constants import Teams

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 1000)

season4 = pd.read_csv('../player_data/phs_2021_1.csv')

sombra = season4[season4['hero_name'] == 'Sombra']

sombra.to_csv('sombra.csv', index=False)

interesting_stats = ['EMP Efficiency', "Enemies EMP'd", 'Enemies Hacked', 'Time Building Ultimate', 'Time Elapsed per Ultimate Earned', 'Time Holding Ultimate', 'Time Played', 'Ultimates Earned - Fractional', 'Ultimates Used']

sombra = sombra[sombra['stat_name'].isin(interesting_stats)]
print(sombra.columns)
sombra_sums = sombra[['team_name', 'player_name', 'stat_name', 'stat_amount']].groupby(by=['team_name', 'player_name', 'stat_name']).sum().reset_index()

sombra_sums = sombra_sums.pivot(index=['team_name', 'player_name'], columns='stat_name', values='stat_amount').fillna(0.0).reset_index()

sombra_sums['Enemies Hacked per 10'] = 10 * sombra_sums['Enemies Hacked'] / ( sombra_sums['Time Played'] / 60 )
sombra_sums['Enemies EMP\'d per 10'] = 10 * sombra_sums['Enemies EMP\'d'] / ( sombra_sums['Time Played'] / 60 )
sombra_sums['Ultimates Earned per 10'] = 10 * sombra_sums['Ultimates Earned - Fractional'] / ( sombra_sums['Time Building Ultimate'] / 60 )

playoff_teams = [Teams.Justice, Teams.Fuel, Teams.Fusion, Teams.Hunters, Teams.Dragons, Teams.Reign, Teams.Gladiators, Teams.Shock]
sombra_sums = sombra_sums[sombra_sums['team_name'].isin(playoff_teams)]
sombra_sums = sombra_sums[sombra_sums['Time Played'] > 600]

plt.figure(figsize=(10, 8))

plt.title('EMP Build Rate vs EMP Efficiency Rate')
for ind in sombra_sums.index:
    row = sombra_sums.loc[ind, :]
    label = row['player_name']
    x = row['Enemies EMP\'d per 10']
    y = row['Ultimates Earned per 10']
    used = row['Time Played']
    team = row['team_name']
    color = Teams.TeamColors[team]
    plt.scatter(x, y, label=label, s=used/50, color=color)


for ind in sombra_sums.index:
    row = sombra_sums.loc[ind, :]
    label = row['player_name']
    x = row['Enemies EMP\'d per 10']
    y = row['Ultimates Earned per 10']
    used = row['Time Played']
    team = row['team_name']
    color = Teams.TeamColors[team]
    plt.text(x*1.005, y*1.005, label, color=color, weight='bold')


plt.xlabel('Enemies EMP\'d per 10')
plt.ylabel('Ultimates Earned per 10')
plt.show()




