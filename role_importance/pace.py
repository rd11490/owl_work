import pandas as pd
import matplotlib.pyplot as plt

from constants import Teams

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 1000)

heroes = pd.read_csv('../player_data/phs-2022.csv')

heroes = heroes[heroes['hero_name'] == 'All Heroes']
heroes = heroes[heroes['stat_name'].isin(['Deaths', 'Final Blows', 'Time Played'])]

pace_stats = heroes[['esports_match_id', 'map_name', 'team_name', 'stat_name', 'amount']].groupby(by=['esports_match_id', 'map_name','team_name', 'stat_name', ]).sum().reset_index()


paces = []
def calculate_pace(group):
    team = group['team_name'].values[0]
    esports_match_id = group['esports_match_id'].values[0]
    map_name = group['map_name'].values[0]

    deaths = group[group['stat_name'] == 'Deaths']['amount'].values[0]
    final_blows = group[group['stat_name'] == 'Final Blows']['amount'].values[0]
    time_played = group[group['stat_name'] == 'Time Played']['amount'].values[0]

    est_fights = (final_blows+deaths)/7.5
    time_played = time_played/5

    pace = 10 * est_fights / (time_played / 60)

    # 10 * cass_sums[stat] / (cass_sums['Time Played'] / 60


    paces.append({
        'team': team,
        'esports_match_id': esports_match_id,
        'map_name': map_name,
        'pace': pace
    })


pace_stats.groupby(by=['esports_match_id', 'map_name', 'team_name']).apply(calculate_pace)
frame = pd.DataFrame(paces)
print(frame.sort_values(by='pace', ascending=False))
