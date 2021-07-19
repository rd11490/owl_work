import warnings

from constants import hero_pools

warnings.simplefilter(action='ignore')

import pandas as pd
import datetime
import os

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)

pd.set_option('display.width', 1000)

csvs = os.listdir('player_data')  # Get all files in the data directory
frames = []


def calc_season(dt):
    parsed = datetime.datetime.strptime(dt, "%m/%d/%Y %H:%M")
    return parsed.date().strftime("%Y")


def determine_meta_group(row):
    season = row['season']
    if season < '2020':
        if 'Title Matches' in row['stage']:
            row['hero_pool_week'] = row['stage'].replace('- Title Matches', '').replace('Title Matches', '').strip() + ' - ' + season
            return row
        else:
            row['hero_pool_week'] = row['stage'] + ' - ' + season
            return row
    else:
        dt = row['start_time']
        parsed = datetime.datetime.strptime(dt, "%m/%d/%Y %H:%M")
        timestamp = parsed.date().strftime("%Y/%m/%d")
        for daterange in hero_pools:
            try:
                if timestamp > daterange['low'] and timestamp < daterange['high']:
                    row['hero_pool_week'] = daterange['pool'] + ' - ' + season
                    return row
            except:
                print(row)
                print(daterange)
    return row


for file in csvs:
    print(file)
    # Read the file in as a CSV
    frame = pd.read_csv('{}/{}'.format('player_data', file))
    # Update column names so that they are consistent across years
    frame = frame.rename(columns={'esports_match_id': 'match_id', 'tournament_title': 'stage', 'player_name': 'player',
                                  'hero_name': 'hero', 'team_name': 'team', 'pelstart_time': 'start_time'})

    frame['season'] = frame['start_time'].apply(calc_season)
    # Add the dataframe to a list
    frames.append(frame)

player_frame = pd.concat(frames)

player_frame = player_frame[(player_frame['stat_name'] == 'Time Played') & (player_frame['hero'] != 'All Heroes')]

player_frame = player_frame.apply(determine_meta_group, axis=1)

play_time_per_week = player_frame[['hero', 'hero_pool_week', 'map_name', 'stat_amount']].groupby(by=['hero_pool_week', 'map_name', 'hero']).sum().reset_index()

def calc_percent_played(group):
    group['played_percentage'] = 6 * group['stat_amount'] / group['stat_amount'].sum()
    return group

print(play_time_per_week.shape)
play_time_per_week = play_time_per_week.groupby(by=['hero_pool_week', 'map_name']).apply(calc_percent_played).reset_index()

pivoted = play_time_per_week.pivot_table(index=['hero_pool_week', 'map_name'], columns=['hero'], values=['played_percentage']).fillna(0.0)
frame = pd.DataFrame(pivoted.to_records())
cols = [c.replace("('played_percentage', '", '').replace("')", '') for c in frame.columns]
frame.columns = cols
print(frame.head(20))
frame.to_csv('results/map_play_pct.csv', index=False)