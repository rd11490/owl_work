import warnings
warnings.simplefilter(action='ignore')

import pandas as pd
import os

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)

pd.set_option('display.width', 1000)

csvs = os.listdir('player_data') # Get all files in the data directory
frames = []

for file in csvs:
    print(file)
    # Read the file in as a CSV
    frame = pd.read_csv('{}/{}'.format('player_data', file))
    # Update column names so that they are consistent across years
    frame=frame.rename(columns={'esports_match_id': 'match_id', 'tournament_title': 'stage', 'player_name': 'player',
                          'hero_name': 'hero', 'team_name': 'team', 'pelstart_time': 'start_time'})
    # Add the dataframe to a list
    frames.append(frame)

# Concat all of the dataframes together
player_frame = pd.concat(frames)


player_frame = player_frame[(player_frame['hero'] == 'All Heroes') & (player_frame['stat_name'] == 'Time Played')][['match_id', 'map_name', 'player', 'team']].drop_duplicates()


def build_player_rows(group):
    team1, team2 = group['team'].unique()
    t1_players = sorted(group[group['team']==team1]['player'].unique())
    t2_players = sorted(group[group['team']==team2]['player'].unique())

    if len(t1_players) != 6 or len(t2_players) != 6:
        print(group)

    team1_p1, team1_p2, team1_p3, team1_p4, team1_p5, team1_p6 = t1_players
    team2_p1, team2_p2, team2_p3, team2_p4, team2_p5, team2_p6 = t2_players

    if group.shape[0] != 12:
        print(group)

    return pd.DataFrame([{
        'team': team1,
        'p1': team1_p1,
        'p2': team1_p2,
        'p3': team1_p3,
        'p4': team1_p4,
        'p5': team1_p5,
        'p6': team1_p6
    },{
        'team': team2,
        'p1': team2_p1,
        'p2': team2_p2,
        'p3': team2_p3,
        'p4': team2_p4,
        'p5': team2_p5,
        'p6': team2_p6
    }])

players_rows = player_frame.groupby(by=['match_id', 'map_name']).apply(build_player_rows).reset_index()
print(players_rows)
players_rows = players_rows[['match_id', 'map_name', 'team', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6']]
players_rows.to_csv('results/map_lineups.csv', index=False)