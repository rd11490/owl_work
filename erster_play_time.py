import warnings
warnings.simplefilter(action='ignore')

import pandas as pd
import datetime
import math
from pytz import timezone


pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def calc_match_date(dt):
    tz = timezone('US/Pacific')
    parsed = datetime.datetime.strptime(dt, "%m/%d/%Y %H:%M").astimezone(tz)
    return parsed.date().strftime("%Y/%m/%d")

def calc_match_week_and_year(dt):
    parsed = datetime.datetime.strptime(dt, "%Y/%m/%d")
    year = parsed.isocalendar()[0]
    week = parsed.isocalendar()[1]
    if week < 10:
        week = '0' + str(week)
    return '{}-{}'.format(year, week)



## PART 1
print('Erster Play Time - Mei')

frame = pd.read_csv('player_data/phs_2020_1.csv')

na_teams = ['Paris Eternal', 'Toronto Defiant',
 'Los Angeles Gladiators',  'Dallas Fuel',
 'Los Angeles Valiant', 'Boston Uprising', 'San Francisco Shock',
 'Florida Mayhem', 'Houston Outlaws', 'Philadelphia Fusion',
 'Washington Justice', 'Atlanta Reign']

mei = frame[(frame['stat_name'] == 'Time Played') & (frame['hero_name'] == 'Mei') & (frame['team_name'] == 'Atlanta Reign')]
mei['game_date'] = mei['start_time'].apply(calc_match_date)
mei['game_week'] = mei['game_date'].apply(calc_match_week_and_year)

atlanta_maps = mei[['esports_match_id', 'map_name', 'player_name', 'stat_name', 'stat_amount', 'hero_name', 'game_week']]

print(atlanta_maps)

total_min = atlanta_maps['stat_amount'].sum()

ptime = atlanta_maps[['player_name', 'stat_amount']].groupby(by='player_name').sum().reset_index()

ptime['pct'] = ptime['stat_amount'] / total_min

print('Percentage of Atlanta Reign Mei Play Time')
ptime.columns = ['player_name', 'time_played', 'pct']
print(ptime)

total_matchs = len(atlanta_maps['esports_match_id'].unique())
match_cnt = atlanta_maps[['player_name', 'esports_match_id']].drop_duplicates().groupby(by=['player_name']).count().reset_index()
match_cnt.columns = ['player_name', 'match_count']
match_cnt['pct'] = match_cnt['match_count'] / total_matchs

print('\n\n')
print('Percentage of Atlanta Reign Matches With Mei Played')
print(match_cnt)

total_maps = atlanta_maps[['esports_match_id', 'map_name']].drop_duplicates().shape[0]
map_cnt = atlanta_maps[['player_name', 'esports_match_id', 'map_name']].drop_duplicates().groupby(by=['player_name']).count().reset_index()
map_cnt = map_cnt[['player_name', 'map_name']]
map_cnt.columns = ['player_name', 'map_count']
map_cnt['pct'] = map_cnt['map_count'] / total_maps


print('\n\n')
print('Percentage of Atlanta Reign Maps With Mei Played')
print(map_cnt)


### PART 2
# How to check if Mei is meta?
# Did mei account for at least 1/12 of play time in a match weekend (1 player on her at all times)
#
print('\n\n')
print('\n\n')

print('Did Atlanta NOT Play Mei when meta')


frame2 = pd.read_csv('data/phs_2020_1.csv')

time_played = frame2[(frame2['stat_name'] == 'Time Played') & (frame2['hero_name'] != 'All Heroes')]

time_played['game_date'] = time_played['start_time'].apply(calc_match_date)
time_played['game_week'] = time_played['game_date'].apply(calc_match_week_and_year)

def play_time_per_match(group):
    total_time = group['stat_amount'].sum()
    group['pct'] = group['stat_amount'] / total_time
    return group

week_pct = time_played.groupby(by='game_week').apply(play_time_per_match).reset_index()
week_pct = week_pct[['hero_name', 'game_week', 'pct']].groupby(by=['game_week', 'hero_name']).sum().reset_index()

mei_week = week_pct[week_pct['hero_name'] == 'Mei']
mei_week['meta'] = mei_week['pct'] >= 1/12
mei_week = mei_week[mei_week['meta']]
mei_week = mei_week[['game_week']]

mei_meta_weeks = mei_week['game_week'].unique()
print('Weeks OWL thought Mei was Meta')
print(mei_meta_weeks)

atlanta_weeks_played = time_played[(time_played['stat_name'] == 'Time Played') & (time_played['team_name'] == 'Atlanta Reign')]
atlanta_weeks_played = atlanta_weeks_played['game_week'].unique()
print('Weeks Atlanta Played')
print(atlanta_weeks_played)

weeks_atlanta_played_mei = time_played[(time_played['stat_name'] == 'Time Played') & (time_played['team_name'] == 'Atlanta Reign')]
weeks_atlanta_played_mei = weeks_atlanta_played_mei.groupby(by='game_week').apply(play_time_per_match).reset_index()
weeks_atlanta_played_mei = weeks_atlanta_played_mei[['hero_name', 'game_week', 'pct']].groupby(by=['game_week', 'hero_name']).sum().reset_index()

atl_mei_week = weeks_atlanta_played_mei[weeks_atlanta_played_mei['hero_name'] == 'Mei']
atl_mei_week['meta'] = atl_mei_week['pct'] >= 1/12
weeks_atlanta_thought_mei_was_meta = atl_mei_week[atl_mei_week['meta']]['game_week'].unique()
print('Weeks Atlanta Thought Mei was Meta')
print(weeks_atlanta_thought_mei_was_meta)


weeks_earter_played = time_played[(time_played['stat_name'] == 'Time Played') & (time_played['team_name'] == 'Atlanta Reign') & (time_played['player_name'] == 'Erster')]['game_week'].unique()
print('Weeks Erster Played')
print(weeks_earter_played)
#
# weeks_atlanta_played_and_mei_meta = set(atlanta_weeks_played).intersection(set(mei_meta_weeks))
# print(weeks_atlanta_played_and_mei_meta)

print('\n\n')
print('\n\n')

# Part 3
#
# Erster Hero Pool
print('Ersters Hero Pool this Season')
weeks_erster_played = time_played[(time_played['stat_name'] == 'Time Played') & (time_played['team_name'] == 'Atlanta Reign') & (time_played['player_name'] == 'Erster')][['hero_name', 'stat_amount']]
total_time_played = weeks_erster_played['stat_amount'].sum()
hero_play_times = weeks_erster_played.groupby('hero_name').sum().reset_index()
hero_play_times['pct'] = hero_play_times['stat_amount']/total_time_played
hero_play_times.columns = ['hero_name', 'play_time', 'pct']
print(hero_play_times)

# Part 4
#
# Erster Hero Pool previous years
print('\n\n')
print('\n\n')
print('Ersters Hero Pool last Season')

frames = []
for i in [1,2,3,4]:
    frame = pd.read_csv('player_data/phs_2019_stage_{}.csv'.format(i))
    frames.append(frame)


all = pd.concat(frames)
weeks_erster_played = all[(all['stat_name'] == 'Time Played') & (all['team'] == 'Atlanta Reign') & (all['player'] == 'Erster') & (all['hero'] != 'All Heroes')][['hero', 'stat_amount']]
total_time_played = weeks_erster_played['stat_amount'].sum()
hero_play_times = weeks_erster_played.groupby('hero').sum().reset_index()
hero_play_times['pct'] = hero_play_times['stat_amount']/total_time_played
hero_play_times.columns = ['hero', 'play_time', 'pct']
print(hero_play_times)