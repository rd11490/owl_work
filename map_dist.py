import pandas as pd

from constants import Maps

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 1000)

frame = pd.read_csv('./map_data/match_map_stats.csv')


def calc_map_type(map_name):
    return Maps.map_types[map_name]

frame['map_type'] = frame['map_name'].apply(calc_map_type)

payload_maps = frame[(frame['map_type'].isin([Maps.Escort, Maps.Hybrid])) & (frame['attacker_round_end_score'] != frame['attacker']) & (frame['attacker_round_end_score'] < 4)][['map_name', 'map_type','attacker_round_end_score','attacker_payload_distance']]
payload_maps = payload_maps.groupby(by=['map_name','attacker_round_end_score']).max().reset_index()

print(payload_maps)

maps = {}

for ind, group in payload_maps.groupby(by='map_name'):
    if group['map_type'].values[0] == Maps.Escort:
        map_name = group['map_name'].values[0]
        maps[(map_name, 0)] = 0.0
        maps[(map_name, 1)] = payload_maps.loc[1, :]['attacker_payload_distance']
        maps[(map_name, 2)] = payload_maps.loc[1, :]['attacker_payload_distance']
        maps[(map_name, 3)] = payload_maps.loc[3, :]['attacker_payload_distance']
    else:
        map_name = group['map_name'].values[0]
        maps[(map_name, 0)] = 0.0
        maps[(map_name, 1)] = payload_maps.loc[0, :]['attacker_payload_distance']
        maps[(map_name, 2)] = payload_maps.loc[1, :]['attacker_payload_distance']
        maps[(map_name, 3)] = payload_maps.loc[3, :]['attacker_payload_distance']

print(maps)

