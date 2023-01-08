import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 1000)

"""
['All Heroes' 'Echo' 'Mei' 'Reaper' 'Sombra' 'Symmetra' 'Reinhardt'
 'Winston' 'Wrecking Ball' 'Ana' 'Baptiste' 'Moira' 'D.Va' 'Brigitte'
 'Lúcio' 'Doomfist' 'Tracer' 'Zenyatta' 'Ashe' 'McCree' 'Sigma' 'Hanzo'
 'Zarya' 'Pharah' 'Widowmaker' 'Orisa' 'Genji' 'Soldier: 76' 'Junkrat'
 'Roadhog' 'Bastion' 'Mercy' 'Torbjörn']
 """
hero_name = 'McCree'

season4 = pd.read_csv('./player_data/phs_2021_1.csv')


hero = season4[season4['hero_name'] == hero_name]

hero.to_csv('{}.csv'.format(hero_name.lower()), index=False)

