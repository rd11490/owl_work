import warnings

warnings.simplefilter(action='ignore')

import pandas as pd
import numpy as np
from itertools import product
import networkx as nx

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

map_lineups = pd.read_csv('results/map_play_pct.csv')

rule_sets = map_lineups['hero_pool_week'].unique()

sets = []

for r in rule_sets:

    rule_group = map_lineups[map_lineups['hero_pool_week'] == r].copy()

    maps = list(rule_group['map_name'].values)

    rule_group = rule_group.set_index('map_name')

    pairs = list(product(maps, maps))

    for (left, right) in pairs:
        if left == right:
            pass
        else:

            left_data = rule_group.loc[left].values[1:-1]
            right_data = rule_group.loc[right].values[1:-1]
            dist = np.linalg.norm(left_data-right_data)
            row = {
                'Hero Pool': r,
                'Map1': left,
                'Map2': right,
                'Distance': dist
            }
            sets.append(row)

frame = pd.DataFrame(sets)

frame.to_csv('results/map_sim.csv', index=False)

# sim_scores = frame[['Map1','Map2','Distance']].groupby(by=['Map1','Map2']).mean().reset_index()
sim_scores = frame.sort_values(by=['Hero Pool', 'Map1', 'Distance'])

print(sim_scores.head(100))

thresholds = [i*.1 for i in range(1, 20)]

def build_graph(edges, thresh):

    nodes = list(edges['Map1'].values)

    filtered = edges[edges['Distance'] < thresh]
    # print(filtered)
    edge_objects = filtered[['Map1','Map2']].to_records(index=False)


    G = nx.Graph()

    for n in nodes:
        G.add_node(n)

    G.add_edges_from(edge_objects)

    return G


for t in thresholds:
    print(t)
    graph = build_graph(sim_scores, t)
    comps = nx.connected_components(graph)
    for c in comps:
        print(c)





# map_lineups['cluster'] = preds
#
# groups = map_lineups[['map_name','cluster']].groupby('map_name')
#
# for g in groups:
#     print(g)

# print(map_lineups[['map_name','cluster']].head(300))
