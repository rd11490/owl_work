import pandas as pd
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 1000)

season4 = pd.read_csv('./player_data/phs_2021_1.csv')

season4 = season4[season4['hero_name'] != 'All Heroes']
hero_stats = season4[['stat_name', 'hero_name']].drop_duplicates().dropna()
print(hero_stats)
