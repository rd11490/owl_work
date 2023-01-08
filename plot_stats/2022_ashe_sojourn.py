import pandas as pd
import matplotlib.pyplot as plt

from constants import Teams

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 1000)

season5 = pd.read_csv('../player_data/phs-2022.csv')

print(season5)

print(season5['stat_name'].unique())


stat_x = 'All Damage Done'
stat_y = 'Final Blows'
size = 'Time Played'
min_size = 12000

def stat_rate(str):
    return '{} Rate'.format(str)

heroes = ['Ashe']

hero_stats = season5[season5['hero_name'].isin(heroes)]


players_and_teams = hero_stats[['player_name', 'team_name']].groupby('player_name').head(1).reset_index()

stats = [stat_x, stat_y, size]

hero_stats = hero_stats[hero_stats['stat_name'].isin(stats)]

print(hero_stats)


def get_first_or_zero(value):
    if len(value) > 0:
        return value[0]
    else:
        return 0.0


def flatten_group(group):
    y_stat = group[group['stat_name'] == stat_y]['amount'].values
    x_stat = group[group['stat_name'] == stat_x]['amount'].values
    size_stat = group[group['stat_name'] == size]['amount'].values

    return pd.Series({
        stat_y: get_first_or_zero(y_stat),
        stat_x: get_first_or_zero(x_stat),
        size: get_first_or_zero(size_stat)
    })


stats = hero_stats[['player_name', 'stat_name', 'amount']].groupby(
    by=['player_name', 'stat_name']).sum().reset_index().groupby(by=['player_name']).apply(flatten_group).reset_index()


stats = stats.merge(players_and_teams, on='player_name')

print(stats)

stats[stat_rate(stat_x)] = 600 * stats[stat_x] / stats[size]
stats[stat_rate(stat_y)] = 600 * stats[stat_y] / stats[size]

stats = stats.sort_values(by=size, ascending=False)
stats = stats[stats[size] > min_size]

print(stats)
plt.figure(figsize=(10, 8))

plt.title('Final Blows  per 10 vs All Damage Done per 10')
for ind in stats.index:
    row = stats.loc[ind, :]
    label = row['player_name']
    x_rate = row[stat_rate(stat_x)]
    y_rate = row[stat_rate(stat_y)]
    used = row[size]
    team = row['team_name']
    color = Teams.TeamColors[team]
    plt.scatter(x_rate, y_rate, label=label, s=used/20, color=color)


for ind in stats.index:
    row = stats.loc[ind, :]
    label = row['player_name']
    x_rate = row[stat_rate(stat_x)]
    y_rate = row[stat_rate(stat_y)]
    team = row['team_name']
    color = Teams.TeamColors[team]
    plt.text(x_rate + 0.5, y_rate + 0.15, label, color=color, weight='bold')


plt.xlabel(stat_x)
plt.ylabel(stat_y)
plt.show()