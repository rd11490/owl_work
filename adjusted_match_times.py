import pandas as pd
import datetime
import matplotlib.pyplot as plt
from utils import calc_match_date, calc_season


from constants import Maps

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)

pd.set_option('display.width', 1000)

frame = pd.read_csv('map_data/match_map_stats.csv')



frame['start_datetime'] = pd.to_datetime(frame['round_start_time'])
frame['end_datetime'] = pd.to_datetime(frame['round_end_time'])

frame['round_time'] = frame['end_datetime'] - frame['start_datetime']
frame['season'] = frame['end_datetime'].apply(lambda x: datetime.datetime.strftime(x, '%Y'))


matches = frame.groupby('match_id')

def filter_extra_maps(group):
    map_results = group[['match_winner', 'map_winner', 'game_number']].drop_duplicates()
    winners = map_results['map_winner']
    match_winner = map_results['match_winner'].iloc[0]
    filter_first_3 = True
    for ind, winner in enumerate(winners):
        if ind < 3:

            filter_first_3 = filter_first_3 and winner == match_winner

    if filter_first_3:
        return group[group['game_number'].isin([1, 2 ,3])]
    else:
        return group


groups = []

for index, match in matches:
    filtered_group = filter_extra_maps(match)
    total_time = filtered_group['round_time'].sum()
    maps_counted = filtered_group['game_number'].max()
    maps_played = match['game_number'].max()

    groups.append({
        'match_id': index,
        'stage': match['stage'].iloc[0],
        'season': match['season'].iloc[0],
        'team_one': match['team_one_name'].iloc[0],
        'team_two': match['team_two_name'].iloc[0],
        'match_winner': match['match_winner'].iloc[0],
        'maps_counted': maps_counted,
        'maps_played': maps_played,
        'total_time': total_time
    })

time_frame = pd.DataFrame(groups)

sorted_frame = time_frame.sort_values(by='total_time', ascending=True)
print(sorted_frame.head(20))
