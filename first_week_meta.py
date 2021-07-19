import pandas as pd
import datetime



pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


season1 = pd.read_csv('./player_data/phs_2018_stage_1.csv')
season2 = pd.read_csv('./player_data/phs_2019_stage_1.csv')
season3 = pd.read_csv('./player_data/phs_2020_1.csv')
season4 = pd.read_csv('./player_data/phs_2021_1.csv')


def calc_match_week_and_year(dt):
    date = dt.split(' ')[0]
    date = date.replace('-','/')
    parsed = datetime.datetime.strptime(date, "%m/%d/%Y")
    year = parsed.isocalendar()[0]
    week = parsed.isocalendar()[1]
    if week < 10:
        week = '0' + str(week)
    return '{}-{}'.format(year, week)

def calc_match_week_and_year_new(dt):
    date = dt.split(' ')[0]
    date = date.replace('-','/')
    parsed = datetime.datetime.strptime(date, "%Y/%m/%d")
    year = parsed.isocalendar()[0]
    week = parsed.isocalendar()[1]
    if week < 10:
        week = '0' + str(week)
    return '{}-{}'.format(year, week)

def calc_season_week(df):
    min = df['week'].minimum()
    df['league_week'] = df['week'] - min
    return df

print(season1)
print(season2)
print(season3)
print(season4)


season1['week']= season1['start_time'].apply(calc_match_week_and_year)
season2['week']= season2['pelstart_time'].apply(calc_match_week_and_year)
season3['week']= season3['start_time'].apply(calc_match_week_and_year)
season4['week']= season4['start_time'].apply(calc_match_week_and_year_new)

season1 = calc_season_week(season1)
season2 = calc_season_week(season2)
season3 = calc_season_week(season3)
season4 = calc_season_week(season4)



print(season1)
print(season2)
print(season3)
print(season4)

