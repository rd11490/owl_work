import pandas as pd
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

scored_maps = pd.read_csv('results/scored_maps.csv')
print(scored_maps)

groups = scored_maps.groupby(by='map_type')
for i, group in groups:
    print(i)
    print(group[['team_one_score', 'team_two_score']].describe())