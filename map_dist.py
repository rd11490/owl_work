import pandas as pd

from constants import Maps

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 1000)

frame = pd.read_csv('data/match_map_stats.csv')


def calc_map_type(map_name):
    return Maps.map_types[map_name]

frame['map_type'] = frame['map_name'].apply(calc_map_type)

payload_maps = frame[(frame['map_type'].isin([Maps.Escort, Maps.Hybrid])) & (frame['attacker_round_end_score'] < 3)][['map_name','attacker_round_end_score','attacker_payload_distance']]
payload_maps = payload_maps.groupby(by=['map_name','attacker_round_end_score']).max().reset_index()

print(payload_maps)

maps = {}

for ind in payload_maps.index:
    row = payload_maps.loc[ind,:]
    maps[(row['map_name'], row['attacker_round_end_score'])] = row['attacker_payload_distance']

print(maps)

