import pandas as pd
import datetime

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

schedule = pd.read_csv('2021_league_schedule.csv')

print(schedule)


def calc_season(dt):
    parsed = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    return parsed.date().strftime("%Y")

match_results = pd.read_csv('match_map_stats.csv')
match_results['season'] = match_results['round_end_time'].apply(calc_season)

print(match_results[match_results['season'] == '2021'])