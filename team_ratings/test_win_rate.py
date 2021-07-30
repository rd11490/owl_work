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

escort_maps = frame[frame['map_type'] == Maps.Escort]
assault_maps = frame[frame['map_type'] == Maps.Assault]
control_maps = frame[frame['map_type'] == Maps.Control]
hybrid_maps = frame[frame['map_type'] == Maps.Hybrid]

tied = escort_maps[(escort_maps['map_round'] == 2) & (escort_maps['attacker_round_end_score'] == 3) & (escort_maps['defender_round_end_score'] == 3)]

tied['attacker_ahead'] = tied['attacker_time_banked'] > tied['defender_time_banked']
tied['attcker_wins'] = tied['map_winner'] == tied['attacker']

tied['both_met'] = tied['attacker_ahead'] == tied['attcker_wins']
print(tied['both_met'].describe())