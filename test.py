import pandas as pd
from constants import Maps, total_escort_map_distance, total_map_time, time_to_add
from utils import calc_match_date, calc_season

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)

pd.set_option('display.width', 1000)

frame = pd.read_csv('./map_data/match_map_stats.csv')


def calc_map_type(map_name):
    return Maps.map_types[map_name]


frame['map_type'] = frame['map_name'].apply(calc_map_type)
frame['match_date'] = frame['round_end_time'].apply(calc_match_date)
frame['season'] = frame['round_end_time'].apply(calc_season)

# print(frame[(frame['winning_team_final_map_score'] == 2) & (frame['losing_team_final_map_score'] == 1) & (frame['map_name'] == 'Temple of Anubis')])

frame = frame[(frame['match_id'] == 37223) & (frame['map_name'] == 'Hanamura')].groupby(by='map_name')


def calculate_assault_map_score(group):
    highest = group['map_round'].max()
    row = group[group['map_round'] == highest]

    team_one = row['attacker'].values[0]
    team_two = row['defender'].values[0]

    team_one_rounds = row['attacker_round_end_score'].values[0]
    team_two_rounds = row['defender_round_end_score'].values[0]

    team_one_rounds_for_time = team_one_rounds
    team_two_rounds_for_time = team_two_rounds

    team_one_time_banked = row['attacker_time_banked'].values[0]
    team_two_time_banked = row['defender_time_banked'].values[0]

    if row['map_winner'].values[0] == team_one and team_one_time_banked > 0.0:
        team_one_rounds_for_time -= 1
    elif row['map_winner'].values[0] == team_two and team_two_time_banked > 0.0:
        team_two_rounds_for_time -= 1

    team_one_total_time = total_map_time(Maps.Assault, team_one_rounds_for_time)
    team_two_total_time = total_map_time(Maps.Assault, team_two_rounds_for_time)

    team_one_rate = team_one_rounds / (team_one_total_time - team_one_time_banked)
    team_two_rate = team_two_rounds / (team_two_total_time - team_two_time_banked)

    if team_one_time_banked > 0.0:
        team_one_rounds_to_add = team_one_rate * team_one_time_banked
        team_one_score = (team_one_rounds_to_add + team_one_rounds) / 2
    else:
        team_one_rounds_to_add = 0
        team_one_score = team_one_rounds / 2

    if team_two_time_banked > 0.0:
        team_two_rounds_to_add = team_two_rate * team_two_time_banked
        team_two_score = (team_two_rounds_to_add + team_two_rounds) / 2
    else:
        team_two_rounds_to_add = 0
        team_two_score = team_two_rounds / 2

    # print('total map distance ', total_map_distance)
    print('team 1: ', team_one)
    print('team 1 score', team_one_score)
    print('team 1 rounds', team_one_rounds)

    # print('team 1 distance', team_one_total_distance)
    print('team 1 time', team_one_total_time)
    print('team 1 time banked', team_one_time_banked)
    print('team 1 time used', team_one_total_time - team_one_time_banked)
    print('team 2: ', team_two)
    print('team 2 score', team_two_score)
    print('team 2 rounds', team_two_rounds)
    print('team 2 rounds to add', team_two_rounds_to_add)

    # print('team 2 distance', team_two_total_distance)
    print('team 2 time', team_two_total_time)
    print('team 2 time banked', team_two_time_banked)
    print('team 2 time used', team_two_total_time - team_two_time_banked)


for group in frame:
    print(group[1])
    calculate_assault_map_score(group[1])
