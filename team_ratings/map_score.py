import pandas as pd
from constants import Maps, total_escort_map_distance, total_map_time, time_to_add
from utils import calc_match_date, calc_season

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)

pd.set_option('display.width', 1000)

frame = pd.read_csv('../map_data/match_map_stats.csv')

def calc_map_type(map_name):
    return Maps.map_types[map_name]


frame['map_type'] = frame['map_name'].apply(calc_map_type)
frame['match_date'] = frame['round_end_time'].apply(calc_match_date)
frame['season'] = frame['round_end_time'].apply(calc_season)

frame = frame[frame['season'] == '2021']

escort_maps = frame[frame['map_type'] == Maps.Escort]
assault_maps = frame[frame['map_type'] == Maps.Assault]
control_maps = frame[frame['map_type'] == Maps.Control]
hybrid_maps = frame[frame['map_type'] == Maps.Hybrid]


###############################
# Calculate control map score #
###############################
# Controls maps are "easy" to score because each team is able to get a control percentage.
# Convert the percentage to a decimal and use it as the map score
def calculate_control_map_score(group):
    # Break out attacker and defender into team 1 and team 2
    team_one = group['attacker'].values[0]
    team_two = group['defender'].values[0]

    # Pull out how many points each team was given credit for capping
    team_one_score = group['attacker_control_perecent'].sum()/200
    team_two_score = group['defender_control_perecent'].sum()/200


    return pd.Series({
        'map_name': group['map_name'].values[0],
        'map_type': group['map_type'].values[0],
        'map_winner': group['map_winner'].values[0],
        'match_date': group['match_date'].values[0],
        'team_one_name': team_one,
        'team_two_name': team_two,
        'team_one_score': team_one_score,
        'team_two_score': team_two_score,
        'season': group['season'].values[0]
    })
###############################
# Calculate Assault map score #
###############################
def calculate_assault_map_score(group):
    # I am limiting this analysis to the intial map parameters (2 rounds) and ignore any tie breaker/overtime scenarios.
    row = group[group['map_round'] == 2]
    # There is some old (bad) data in the dataset that needs to be cleaned. This line cleans that for us.
    if row.empty:
        row = group[group['map_round'] == group['map_round'].max()]

    # Break out attacker and defender into team 1 and team 2
    team_one = row['attacker'].values[0]
    team_two = row['defender'].values[0]

    # Pull out the number of points each team captured
    team_one_points = row['attacker_round_end_score'].values[0]
    team_two_points = row['defender_round_end_score'].values[0]

    # Pull out the amount of team each team banked if they completed the map
    team_one_time_banked = row['attacker_time_banked'].values[0]
    team_two_time_banked = row['defender_time_banked'].values[0]

    # When determining how much time each team had available we need to pull out the number of points they captured.
    # We can calculate that based on the rule set for the map type.
    # For Assault: 4 Minutes to attack point 1, an additional 4 minutes to attack point 2
    team_one_points_for_time = team_one_points
    team_two_points_for_time = team_two_points

    # There is an important exception here. If the winning team does not full cap the map, the number of points
    # they are given credit for is 1 more than they had actually capped.
    # We need to subtract that additional point from their score to properly account for how much time the team used.
    if row['map_winner'].values[0] == team_one:
        team_one_points_for_time -= 1
    elif row['map_winner'].values[0] == team_two and team_two_time_banked > 0.0:
        team_two_points_for_time -= 1

    team_one_total_time = total_map_time(Maps.Assault, team_one_points_for_time)
    team_two_total_time = total_map_time(Maps.Assault, team_two_points_for_time)

    team_one_rate = team_one_points / (team_one_total_time - team_one_time_banked)
    team_two_rate = team_two_points / (team_two_total_time - team_two_time_banked)

    if team_one_time_banked > 0.0:
        team_one_points_to_add = team_one_rate * team_one_time_banked
        team_one_score = (team_one_points_to_add + team_one_points) / 2
    else:
        team_one_points_to_add = 0
        team_one_score = team_one_points / 2

    if team_two_time_banked > 0.0:
        team_two_points_to_add = team_two_rate * team_two_time_banked
        team_two_score = (team_two_points_to_add + team_two_points) / 2
    else:
        team_two_points_to_add = 0
        team_two_score = team_two_points / 2

    return pd.Series({
        'map_name': row['map_name'].values[0],
        'map_type': row['map_type'].values[0],
        'map_winner': row['map_winner'].values[0],
        'match_date': row['match_date'].values[0],
        'team_one_name': team_one,
        'team_two_name': team_two,
        'team_one_score': team_one_score,
        'team_two_score': team_two_score,
        'season': row['season'].values[0]
    })

assault_scores = assault_maps.groupby(by=['match_id', 'game_number']).apply(calculate_assault_map_score).reset_index()

###############################
# Calculate Payload map score #
###############################
# The basic idea behind our calculation for map score for escort maps is
# "What percentage of an escort map could a team complete at the rate at which they pushed the payload initially".
# We can do this by calculating the total distance the payload traveled, add any additional distance using
# the time banked and the rate at which the team pushed the payload, and dividing by the total distance for the map.

def calculate_payload_map_score(group):
    # I am limiting this analysis to the intial map parameters (2 rounds) and ignore any tie breaker/overtime scenarios.
    row = group[group['map_round'] == 2]
    # There is some old (bad) data in the dataset that needs to be cleaned. This line cleans that for us.
    if row.empty:
        row = group[group['map_round'] == group['map_round'].max()]

    # Pull out the map name
    map_name = row['map_name'].values[0]

    # Break out attacker and defender into team 1 and team 2
    team_one = row['attacker'].values[0]
    team_two = row['defender'].values[0]

    # Pull out how many points each team was given credit for capping
    team_one_points = row['attacker_round_end_score'].values[0]
    team_two_points = row['defender_round_end_score'].values[0]

    # Pull out how much time each team banked if they finished the map
    team_one_time_banked = row['attacker_time_banked'].values[0]
    team_two_time_banked = row['defender_time_banked'].values[0]

    # pull out how much distance each team traveled past their final capture point (if they did not complete the map)
    team_one_distance = row['attacker_payload_distance'].values[0]
    team_two_distance = row['defender_payload_distance'].values[0]

    # There is an important exception here. If the winning team does not full cap the map, the number of points
    # they are given credit for is 1 more than they had actually capped.
    # We need to subtract that additional point to properly account for how much time the team used
    # and how far they actually pushed the payload. We also need to account for the case of a tie. If the team full
    # caps the map, we do not need to include that value as we are already
    # adding the distance the team traveled at that point.
    team_one_points_for_distance = team_one_points
    team_one_points_for_time = team_one_points

    team_two_points_for_distance = team_two_points
    team_two_points_for_time = team_two_points

    if team_one_points == 3:
        team_one_points_for_distance -= 1
    if (team_one_points == 1 and team_one_distance == 0) or (
            row['map_winner'].values[0] == team_one and team_one_time_banked > 0.0):
        team_one_points_for_time -= 1
    if team_two_points == 3:
        team_two_points_for_distance -= 1
    if (team_two_points == 1 and team_two_distance == 0) or (
            row['map_winner'].values[0] == team_two and team_two_time_banked > 0.0):
        team_two_points_for_time -= 1

    # We add the distance up until the previous capped point and the distance traveled at the current point together
    # to get the total distance traveled
    team_one_total_distance = total_escort_map_distance(map_name, team_one_points_for_distance) + team_one_distance
    team_two_total_distance = total_escort_map_distance(map_name, team_two_points_for_distance) + team_two_distance

    # We need to calculate the total amount of time each team had on their push.
    team_one_total_time = total_map_time(Maps.Escort, team_one_points_for_time)
    team_two_total_time = total_map_time(Maps.Escort, team_two_points_for_time)

    # Calculate the rate at which the attacking team pushed the payload
    team_one_rate = team_one_total_distance / (team_one_total_time - team_one_time_banked)
    team_two_rate = team_two_total_distance / (team_two_total_time - team_two_time_banked)

    # If the team banked time, we want to give them credit for it. We do this by applying their cap rate to their banked
    # time to estimate how much farther they could have pushed the payload had they continued at their current rate.
    if team_one_time_banked > 0.0:
        team_one_score = team_one_total_distance + (team_one_rate * team_one_time_banked)
    else:
        team_one_score = team_one_total_distance

    if team_two_time_banked > 0.0:
        team_two_score = team_two_total_distance + (team_two_rate * team_two_time_banked)
    else:
        team_two_score = team_two_total_distance

    # Finally we normalize by total map distance in order to get to map completion percentage
    total_map_distance = total_escort_map_distance(map_name, 3)
    team_one_score = team_one_score / total_map_distance
    team_two_score = team_two_score / total_map_distance

    return pd.Series({
        'map_name': map_name,
        'map_type': row['map_type'].values[0],
        'map_winner': row['map_winner'].values[0],
        'match_date': row['match_date'].values[0],
        'team_one_name': team_one,
        'team_two_name': team_two,
        'team_one_score': team_one_score,
        'team_two_score': team_two_score,
        'season': row['season'].values[0]
    })

control_maps_score = control_maps.groupby(by=['match_id', 'game_number']).apply(calculate_control_map_score).reset_index()


escort_maps_score = escort_maps.groupby(by=['match_id', 'game_number']).apply(calculate_payload_map_score).reset_index()

hybrid_maps_score = hybrid_maps.groupby(by=['match_id', 'game_number']).apply(calculate_payload_map_score).reset_index()

scored_maps = pd.concat([control_maps_score, hybrid_maps_score, escort_maps_score, assault_scores])

scored_maps.to_csv('results/scored_maps.csv', index=False)