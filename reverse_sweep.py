import pandas as pd

from constants import Maps

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 1000)

frame = pd.read_csv('./map_data/match_map_stats.csv')

print(frame)
frame = frame[['stage', 'match_id', 'game_number', 'match_winner', 'map_winner', 'map_loser']]
frame = frame[frame['map_winner'] != 'draw']
frame = frame.drop_duplicates()


def check_sweep(group):
    group['reverse_sweep'] = 'None'
    map_winners = group['map_winner'].values
    if len(map_winners) == 5:
        if map_winners[0] == map_winners[1]:
            if (map_winners[0] != map_winners[2]) and (map_winners[2] == map_winners[3]):
                if map_winners[0] == map_winners[4]:
                    group['reverse_sweep'] = 'DENIED'
                elif map_winners[2] == map_winners[4]:
                    group['reverse_sweep'] = 'GRANTED'
    return group


frame = frame.groupby(by=['stage', 'match_id']).apply(check_sweep).reset_index()
frame = frame[frame['reverse_sweep'] != 'None']
frame = frame[['stage', 'match_id', 'match_winner', 'reverse_sweep']]
frame = frame.drop_duplicates()

total = frame.shape[0]
granted = frame[frame['reverse_sweep'] == 'GRANTED'].shape[0]
denied = frame[frame['reverse_sweep'] == 'DENIED'].shape[0]

print('total', total)
print('granted', granted)
print('denied', denied)

print(frame.groupby(by=['match_winner', 'reverse_sweep']).count())
