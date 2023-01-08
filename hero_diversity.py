import pandas as pd
import datetime
import math

from plots_2021.constants import Teams

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

frame = pd.read_csv('player_data/phs_2021_1.csv')

frame = frame[frame['team_name'].isin(Teams.West)]

play_time = frame[(frame['stat_name'] == 'Time Played') & (frame['hero_name'] != 'All Heroes')]


def calc_match_date(dt):
    parsed = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    return parsed.date().strftime("%Y/%m/%d")


def calc_match_week_and_year(dt):
    parsed = datetime.datetime.strptime(dt, "%Y/%m/%d")
    year = parsed.isocalendar()[0]
    week = parsed.isocalendar()[1]
    if week < 10:
        week = '0' + str(week)
    return '{}-{}'.format(year, week)


play_time['game_date'] = play_time['start_time'].apply(calc_match_date)
play_time['game_week'] = play_time['game_date'].apply(calc_match_week_and_year)


def calc_play_type_stats(group):
    tot_time = group['stat_amount'].sum()
    play_pct = group.groupby(['hero_name'])['stat_amount'].sum().reset_index()
    play_pct['played percent'] = play_pct['stat_amount'] / (tot_time / 6)
    obj = {}
    for i in play_pct.index:
        obj[play_pct.loc[i, 'hero_name']] = play_pct.loc[i, 'played percent']
    return obj


groups = play_time.groupby(by=['game_week']).apply(calc_play_type_stats)

rows = []
for date_ind in groups.index:
    obj = groups[date_ind]
    obj['game_week'] = date_ind
    rows.append(obj)

frame = pd.DataFrame(rows)
frame = frame.fillna(0.0)
# frame = frame.set_index('game_week')

print(frame)
print(frame[frame['Reinhardt'] > 0.4])

# 7 weeks above 40%

print(frame[(frame['Reinhardt'] > frame['Winston']) & (frame['Reinhardt'] > frame['Wrecking Ball']) & (
            frame['Reinhardt'] > frame['Orisa'])])

# print(week_dist[week_dist['Reinhardt'] > 0.4])
