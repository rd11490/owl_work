import warnings
warnings.simplefilter(action='ignore')

from constants import Maps, total_map_time, total_escort_map_distance
import pandas as pd
import datetime
from utils import calc_match_date, calc_season


pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)

pd.set_option('display.width', 1000)

frame = pd.read_csv('map_data/match_map_stats.csv')

def calc_map_type(map_name):
    return Maps.map_types[map_name]


frame['map_type'] = frame['map_name'].apply(calc_map_type)
frame['match_date'] = frame['round_end_time'].apply(calc_match_date)
frame['season'] = frame['round_end_time'].apply(calc_season)

escort_maps = frame[frame['map_type'] == Maps.Escort]
assault_maps = frame[frame['map_type'] == Maps.Assault]
control_maps = frame[frame['map_type'] == Maps.Control]
hybrid_maps = frame[frame['map_type'] == Maps.Hybrid]


###############################
# Calculate control map score #
###############################
control_maps['team_one_score'] = control_maps['attacker_control_perecent'] * (1/3)
control_maps['team_two_score'] = control_maps['defender_control_perecent'] * (1/3)


def calculate_control_map_score(group):
    team_one = group['attacker'].values[0]
    team_two = group['defender'].values[0]

    team_one_score = group['team_one_score'].sum()
    team_two_score = group['team_two_score'].sum()


    return pd.Series({
        'map_name': group['map_name'].values[0],
        'map_winner': group['map_winner'].values[0],
        'match_date': group['match_date'].values[0],
        'team_one_name': team_one,
        'team_two_name': team_two,
        'team_one_score': team_one_score,
        'team_two_score': team_two_score,
        'season': group['season'].values[0]
    })

control_maps_score = control_maps.groupby(by=['match_id', 'game_number']).apply(calculate_control_map_score).reset_index()


control_maps_score = control_maps_score[['match_id', 'game_number','map_name', 'map_winner', 'match_date',  'team_one_name', 'team_two_name', 'team_one_score', 'team_two_score', 'season']]
print(control_maps_score)

###############################
# Calculate Assault map score #
###############################

def calculate_assault_map_score(group):
    highest = group['map_round'].max()
    row = group[group['map_round'] == highest]

    team_one = row['attacker'].values[0]
    team_two = row['defender'].values[0]
    team_one_rounds = row['attacker_round_end_score'].values[0]
    team_two_rounds = row['defender_round_end_score'].values[0]

    team_one_total_time = total_map_time(Maps.Assault, team_one_rounds)
    team_two_total_time = total_map_time(Maps.Assault, team_two_rounds)

    team_one_time_banked = row['attacker_time_banked'].values[0]
    team_two_time_banked = row['defender_time_banked'].values[0]

    team_one_score = team_one_rounds / (team_one_total_time - team_one_time_banked)
    team_two_score = team_two_rounds / (team_two_total_time - team_two_time_banked)

    if team_one_score > team_two_score:
        team_one_score_percent = team_one_score / team_one_score
        team_two_score_percent = team_two_score / team_one_score
    else:
        team_one_score_percent = team_one_score / team_two_score
        team_two_score_percent = team_two_score / team_two_score


    return pd.Series({
        'map_name': row['map_name'].values[0],
        'map_winner': row['map_winner'].values[0],
        'match_date': row['match_date'].values[0],
        'team_one_name': team_one,
        'team_two_name': team_two,
        'team_one_score': 100*team_one_score_percent,
        'team_two_score': 100*team_two_score_percent,
        'season': row['season'].values[0]
    })

assault_scores = assault_maps.groupby(by=['match_id', 'game_number']).apply(calculate_assault_map_score).reset_index()
print(assault_scores)

###############################
# Calculate Escort map score #
###############################


def calculate_escort_map_score(group):
    highest = group['map_round'].max()
    row = group[group['map_round'] == highest]

    map = row['map_name'].values[0]

    team_one = row['attacker'].values[0]
    team_two = row['defender'].values[0]
    team_one_rounds = row['attacker_round_end_score'].values[0]
    team_two_rounds = row['defender_round_end_score'].values[0]

    team_one_time_banked = row['attacker_time_banked'].values[0]
    team_two_time_banked = row['defender_time_banked'].values[0]

    team_one_distance = row['attacker_payload_distance'].values[0]
    team_two_distance = row['defender_payload_distance'].values[0]


    if row['map_winner'].values[0] == team_one and team_one_distance > 0.0:
        team_one_rounds -= 1
    elif row['map_winner'].values[0] == team_two and team_two_distance > 0.0:
        team_two_rounds -= 1

    team_one_total_distance = total_escort_map_distance(map, team_one_rounds) + team_one_distance
    team_two_total_distance = total_escort_map_distance(map, team_two_rounds) + team_two_distance

    team_one_total_time = total_map_time(Maps.Escort, team_one_rounds)
    team_two_total_time = total_map_time(Maps.Escort, team_two_rounds)



    team_one_score = team_one_total_distance / (team_one_total_time - team_one_time_banked)
    team_two_score = team_two_total_distance / (team_two_total_time - team_two_time_banked)

    if team_one_score > team_two_score:
        team_one_score_percent = team_one_score / team_one_score
        team_two_score_percent = team_two_score / team_one_score
    else:
        team_one_score_percent = team_one_score / team_two_score
        team_two_score_percent = team_two_score / team_two_score


    return pd.Series({
        'map_name': map,
        'map_winner': row['map_winner'].values[0],
        'match_date': row['match_date'].values[0],
        'team_one_name': team_one,
        'team_two_name': team_two,
        'team_one_score': 100*team_one_score_percent,
        'team_two_score': 100*team_two_score_percent,
        'season': row['season'].values[0]
    })

escort_maps_score = escort_maps.groupby(by=['match_id', 'game_number']).apply(calculate_escort_map_score).reset_index()

print(escort_maps_score)

###############################
# Calculate Hybrid map score #
###############################


def calculate_hybrid_map_score(group):
    highest = group['map_round'].max()
    row = group[group['map_round'] == highest]

    map = row['map_name'].values[0]

    team_one = row['attacker'].values[0]
    team_two = row['defender'].values[0]
    team_one_rounds = row['attacker_round_end_score'].values[0]
    team_two_rounds = row['defender_round_end_score'].values[0]

    team_one_time_banked = row['attacker_time_banked'].values[0]
    team_two_time_banked = row['defender_time_banked'].values[0]

    team_one_distance = row['attacker_payload_distance'].values[0]
    team_two_distance = row['defender_payload_distance'].values[0]


    if row['map_winner'].values[0] == team_one and team_one_distance > 0.0:
        team_one_rounds -= 1
    elif row['map_winner'].values[0] == team_two and team_two_distance > 0.0:
        team_two_rounds -= 1

    team_one_total_distance = total_escort_map_distance(map, team_one_rounds) + team_one_distance
    team_two_total_distance = total_escort_map_distance(map, team_two_rounds) + team_two_distance

    team_one_total_time = total_map_time(Maps.Escort, team_one_rounds)
    team_two_total_time = total_map_time(Maps.Escort, team_two_rounds)



    team_one_score = team_one_total_distance / (team_one_total_time - team_one_time_banked)
    team_two_score = team_two_total_distance / (team_two_total_time - team_two_time_banked)

    if team_one_score > team_two_score:
        team_one_score_percent = team_one_score / team_one_score
        team_two_score_percent = team_two_score / team_one_score
    else:
        team_one_score_percent = team_one_score / team_two_score
        team_two_score_percent = team_two_score / team_two_score


    return pd.Series({
        'map_name': map,
        'map_winner': row['map_winner'].values[0],
        'match_date': row['match_date'].values[0],
        'team_one_name': team_one,
        'team_two_name': team_two,
        'team_one_score': 100*team_one_score_percent,
        'team_two_score': 100*team_two_score_percent,
        'season': row['season'].values[0]
    })

hybrid_maps_score = hybrid_maps.groupby(by=['match_id', 'game_number']).apply(calculate_hybrid_map_score).reset_index()

scored_maps = pd.concat([control_maps_score, hybrid_maps_score, escort_maps_score, assault_scores])

scored_maps.to_csv('results/scored_maps_bk.csv', index=False)