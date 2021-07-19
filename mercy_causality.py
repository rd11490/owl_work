import pandas as pd
import datetime

from constants import Maps

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


player_stats = pd.read_csv('player_data/phs_2020_2.csv')
mercy_stats = player_stats[player_stats['hero_name'] == 'Mercy']

print(mercy_stats)

map_scores = pd.read_csv('results/scored_maps.csv')
print(map_scores)