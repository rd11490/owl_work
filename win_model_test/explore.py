import pandas as pd
import numpy as np
from re import split



pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 1000)

frame = pd.read_json('data/v2_jsonl_teams.json', lines=True)

player_frame_arr = []
match_frame_arr = []

bad_data = 0
for i in frame.index:
    row = frame.iloc[i, :]
    teams = row['teams']
    if 'blue' not in teams or 'red' not in teams:
        bad_data += 1
        continue

    blue = teams['blue']
    red = teams['red']
    blue_result = row['result']

    if blue_result not in ['WIN', 'LOSS'] or len(red) != 6 or len(blue) != 6:
        bad_data += 1
        continue

    red_result = 'LOSS' if blue_result == 'WIN' else 'WIN'

    for p in blue:
        if not pd.isnull(p):
            player_frame_arr.append({
                'game_id': i,
                'result': blue_result,
                'player': p
            })


    for p in red:
        if not pd.isnull(p):
            player_frame_arr.append({
                'game_id': i,
                'result': red_result,
                'player': p
            })


    match_frame_arr.append({
        'game_id': i,
        'result': blue_result,

        'b1': blue[0],
        'b2': blue[1],
        'b3': blue[2],
        'b4': blue[3],
        'b5': blue[4],
        'b6': blue[5],

        'r1': red[0],
        'r2': red[1],
        'r3': red[2],
        'r4': red[3],
        'r5': red[4],
        'r6': red[5]
    })

players_frame = pd.DataFrame(player_frame_arr)

player_games = players_frame[['player', 'result']].groupby('player').count().reset_index()
print(player_games)
print(player_games['result'].mean())
print(player_games[player_games['result'] == 1])
print(player_games.describe())

players_more_than_1 = list(player_games[player_games['result'] > 1]['player'])
print(len(players_more_than_1))

match_frame = pd.DataFrame(match_frame_arr)
print(match_frame.shape)

match_frame_duplicates = match_frame[
    (match_frame['b1'].isin(players_more_than_1)) &
    (match_frame['b2'].isin(players_more_than_1)) &
    (match_frame['b3'].isin(players_more_than_1)) &
    (match_frame['b4'].isin(players_more_than_1)) &
    (match_frame['b5'].isin(players_more_than_1)) &
    (match_frame['b6'].isin(players_more_than_1)) &
    (match_frame['r1'].isin(players_more_than_1)) &
    (match_frame['r2'].isin(players_more_than_1)) &
    (match_frame['r3'].isin(players_more_than_1)) &
    (match_frame['r4'].isin(players_more_than_1)) &
    (match_frame['r5'].isin(players_more_than_1)) &
    (match_frame['r6'].isin(players_more_than_1))
]

print(match_frame_duplicates)
print(match_frame_duplicates.shape)