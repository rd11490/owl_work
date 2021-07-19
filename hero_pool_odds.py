import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)



hero_role = [
    {
        'hero_name': 'Ana',
        'role': 'Support',
        'subRole': 'Flex Support'
    },
    {
        'hero_name': 'Ashe',
        'role': 'DPS',
        'subRole': 'Hitscan'
    }, {
        'hero_name': 'Baptiste',
        'role': 'Support',
        'subRole': 'Flex Support'
    }, {
        'hero_name': 'Bastion',
        'role': 'DPS',
        'subRole': 'Hitscan'
    }, {
        'hero_name': 'Brigitte',
        'role': 'Support',
        'subRole': 'Main Support'
    }, {
        'hero_name': 'D.Va',
        'role': 'Tank',
        'subRole': 'Off Tank'
    }, {
        'hero_name': 'Doomfist',
        'role': 'DPS',
        'subRole': 'Flex DPS'
    }, {
        'hero_name': 'Echo',
        'role': 'DPS',
        'subRole': 'Flex DPS'
    }, {
        'hero_name': 'Genji',
        'role': 'DPS',
        'subRole': 'Flex DPS'
    }, {
        'hero_name': 'Hanzo',
        'role': 'DPS',
        'subRole': 'Flex DPS'
    }, {
        'hero_name': 'Junkrat',
        'role': 'DPS',
        'subRole': 'Flex DPS'
    }, {
        'hero_name': 'Lúcio',
        'role': 'Support',
        'subRole': 'Main Support'
    }, {
        'hero_name': 'McCree',
        'role': 'DPS',
        'subRole': 'Hitscan'
    }, {
        'hero_name': 'Mei',
        'role': 'DPS',
        'subRole': 'Flex DPS'
    }, {
        'hero_name': 'Mercy',
        'role': 'Support',
        'subRole': 'Main Support'
    }, {
        'hero_name': 'Moira',
        'role': 'Support',
        'subRole': 'Flex Support'
    }, {
        'hero_name': 'Orisa',
        'role': 'Tank',
        'subRole': 'Main Tank'
    }, {
        'hero_name': 'Pharah',
        'role': 'DPS',
        'subRole': 'Flex DPS'
    }, {
        'hero_name': 'Reaper',
        'role': 'DPS',
        'subRole': 'Flex DPS'
    }, {
        'hero_name': 'Reinhardt',
        'role': 'Tank',
        'subRole': 'Main Tank'
    }, {
        'hero_name': 'Roadhog',
        'role': 'Tank',
        'subRole': 'Off Tank'
    }, {
        'hero_name': 'Sigma',
        'role': 'Tank',
        'subRole': 'Off Tank'
    }, {
        'hero_name': 'Soldier: 76',
        'role': 'DPS',
        'subRole': 'Hitscan'
    }, {
        'hero_name': 'Sombra',
        'role': 'DPS',
        'subRole': 'Flex DPS'
    }, {
        'hero_name': 'Symmetra',
        'role': 'DPS',
        'subRole': 'Flex DPS'
    }, {
        'hero_name': 'Torbjörn',
        'role': 'DPS',
        'subRole': 'Flex DPS'
    }, {
        'hero_name': 'Tracer',
        'role': 'DPS',
        'subRole': 'Flex DPS'
    }, {
        'hero_name': 'Widowmaker',
        'role': 'DPS',
        'subRole': 'Hitscan'
    }, {
        'hero_name': 'Winston',
        'role': 'Tank',
        'subRole': 'Main Tank'
    }, {
        'hero_name': 'Wrecking Ball',
        'role': 'Tank',
        'subRole': 'Main Tank'
    }, {
        'hero_name': 'Zarya',
        'role': 'Tank',
        'subRole': 'Off Tank'
    }, {
        'hero_name': 'Zenyatta',
        'role': 'Support',
        'subRole': 'Flex Support'
    }
]

hero_role_df = pd.DataFrame(hero_role)




frame2 = pd.read_csv('player_data/phs_2021_1.csv')

time_played = frame2[(frame2['stat_name'] == 'Time Played') & (frame2['hero_name'] != 'All Heroes')]


def play_time_per_match(group):
    total_time = group['stat_amount'].sum()
    group['pct'] = 6 * group['stat_amount'] / total_time
    return group


week_pct = play_time_per_match(time_played)
week_pct = week_pct[['hero_name', 'pct']].groupby(by=['hero_name']).sum().reset_index()


week_pct = week_pct.merge(hero_role_df, on='hero_name')
bannable = week_pct[week_pct['pct']> 1/10]

def normalize(group):
    total_time = group['pct'].sum()
    group['ban_odds'] = group['pct'] / total_time
    return group

roles = bannable.groupby('role').apply(normalize).reset_index().groupby('role')

for i, r in roles:
    print(r.sort_values(by='ban_odds', ascending=False))
