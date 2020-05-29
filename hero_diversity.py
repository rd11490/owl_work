import pandas as pd
import datetime
import math

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

frame = pd.read_csv('data/phs_2020_1.csv')


play_time = frame[(frame['stat_name'] == 'Time Played') & (frame['hero_name'] != 'All Heroes')]

def calc_match_date(dt):
    parsed = datetime.datetime.strptime(dt, "%m/%d/%Y %H:%M")
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
frame = frame.set_index('game_week')



week_dist = {}
week_dist_perfect = {}

print(frame)

def calc_dist(left, right):
    tot = 0.0
    for key in left.keys():
        tot += (left[key] - right[key])**2
    return math.sqrt(tot)


def calc_dist_perfect(left):
    tot = 0.0
    perfect = 6.0/len(left.keys())
    for key in left.keys():
        tot += (left[key] - perfect)**2
    return math.sqrt(tot)


for i in frame.index:
    week_dist[i] = []
    week_dist_perfect[i] = []
    week_stats = frame.loc[i]
    week_dist_perfect[i].append(calc_dist_perfect(week_stats))
    for j in frame.index:
        if i != j:
            other_stats = frame.loc[j]
            week_dist[i].append(calc_dist(week_stats, other_stats))
print(week_dist)


avgs = []
for k in week_dist.keys():
    avgs.append({'week': k, 'avg dist': sum(week_dist[k])/len(week_dist[k])})

avg_frame = pd.DataFrame(avgs)
print(avg_frame)


avgs_perf = []
for k in week_dist_perfect.keys():
    avgs_perf.append({'week': k, 'avg dist': sum(week_dist_perfect[k])/len(week_dist_perfect[k])})

avg_perf_frame = pd.DataFrame(avgs_perf)
print(avg_perf_frame)

