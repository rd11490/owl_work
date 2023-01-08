import pandas as pd
import numpy as np
from re import split



pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 1000)


def camelize(string):
 s = ''.join([a.capitalize() for a in split('([^a-zA-Z0-9])', string) if a.isalnum()])
 return s[0].lower() + s[1:]


frame = pd.read_csv('./out/hero_data_bk.csv')
print(frame['Stat'].unique())

stats_to_care = ['All Damage Done',
 'Critical Hits', 'Damage - Sticky Bombs', 'Damage - Weapon', 'Damage Taken',
 'Deaths', 'Healing Received', 'Hero Damage Done', 'Quick Melee Ticks',
 'Shots Fired', 'Shots Hit', 'Shots Missed',
 'Sticky Bombs Direct Hits',
 'Sticky Bombs Useds', 'Time Alive', 'Time Building Ultimate',
 'Time Played',
 'Ultimates Earned - Fractional', 'Assists',
 'Barrier Damage Done', 'Blizzard Kills',
 'Damage - Blizzard', 'Damage - Weapon Primary', 'Damage - Weapon Secondary',
 'Damage Blocked', 'Eliminations', 'Enemies Frozen', 'Freeze Spray Damage',
 'Icicle Damage', 'Objective Time', 'Offensive Assists', 'Self Healing',
 'Successful Freezes', 'Time Hacked',
 'Time Holding Ultimate', 'Total Time Frozen', 'Ultimates Used',
 'Damage - EMP', 'Damage - Quick Melee', "Enemies EMP'd",
 'Enemies Hacked', 'Final Blows', 'Objective Kills',
 'Quick Melee Hits', 'Time Discorded',
 'Players Teleported', 'Teleporter Uptime', 'Teleporters Placed',
 'Damage - Charge', 'Damage - Earthshatter', 'Damage - Fire Strike',
 'Earthshatter Stuns',
 'Rocket Hammer Melee Hits',
 'Rocket Hammer Melee Hits - Multiple', 'Rocket Hammer Melee Ticks',
 'Damage - Jump Pack', 'Damage - Primal Rage Leap',
 'Damage - Primal Rage Melee', 'Damage - Primal Rage Total',
 'Environmental Kills', 'Jump Pack Kills', 'Knockback Kills',
 'Melee Final Blows', 'Melee Kills', 'Players Knocked Back',
 'Primal Rage Kills',
 'Primal Rage Melee Hits',
 'Primal Rage Melee Hits - Multiple', 'Primal Rage Melee Ticks',
 'Tesla Cannon Hits',
 'Tesla Cannon Hits - Multiple', 'Tesla Cannon Ticks', 'Weapon Kills',
 'Grappling Claw Uses', 'Roll Uptime', 'Roll Uses',
 'Biotic Grenade Kills', 'Damage - Biotic Grenade', 'Damage - Weapon Scoped',
 'Defensive Assists', 'Healing - Biotic Grenade', 'Healing - Weapon',
 'Healing - Weapon Scoped', 'Healing Amplified', 'Healing Done',
 'Nano Boost Assists', 'Nano Boosts Applied',
 'Scoped Hits', 'Scoped Shots', 'Sleep Dart Shots',
 'Unscoped Hits', 'Unscoped Shots',
 'Amplification Matrix Casts', 'Biotic Launcher Healing Explosions',
 'Biotic Launcher Healing Shots', 'Damage Prevented',
 'Healing - Biotic Launcher', 'Healing - Regenerative Burst',
 'Biotic Orb Maximum Damage',
 'Biotic Orb Maximum Healing', 'Coalescence Healing', 'Coalescence Kills',
 'Damage - Biotic Orb', 'Damage - Coalescence', 'Healing - Biotic Orb',
 'Healing - Coalescence', 'Healing - Secondary Fire',
 'Secondary Fire Hits', 'Secondary Fire Ticks',
 'Damage - Boosters', 'Damage - Micro Missiles', 'Damage - Pistol',
 'Environmental Deaths', 'Mech Deaths', 'Mechs Called', 'Self-Destructs',
 'Ultimates Negated', 'Armor - Rally', 'Armor Provided',
 'Damage - Shield Bash', 'Healing - Inspire', 'Healing - Repair Pack',
 'Inspire Uptime',
 'Amped Heal Activations', 'Amped Speed Activations',
 'Heal Song Time Elapsed', 'Healing - Healing Boost',
 'Healing - Healing Boost Amped', 'Sound Barrier Casts',
 'Sound Barriers Provided', 'Soundwave Kills',
 'Speed Song Time Elapsed', 'Ability Damage Done', 'Damage - Meteor Strike',
 'Damage - Rising Uppercut', 'Damage - Rocket Punch',
 'Damage - Seismic Slam', 'Shields Created', 'Damage - Pulse Bomb',
 'Health Recovered', 'Match Blinks Used',
 'Pulse Bomb Kills', 'Pulse Bombs Attached',
 'Recalls Used', 'Critical Hit Kills', 'Damage - Dragonstrike',
 'Damage - Sonic', 'Damage - Storm Arrows',
 'Dragonstrike Kills', 'Recon Assists',
 'Solo Kills', 'Storm Arrow Kills', 'Charge Kills',
 'Earthshatter Kills', 'Fire Strike Kills', 'Multikills',
 'Damage - Self Destruct', 'Damage - Graviton Surge',
 'Energy Maximum', 'Graviton Surge Kills',
 'High Energy Kills', 'Lifetime Energy Accumulation',
 'Primary Fire Hits', 'Primary Fire Ticks',
 'Projected Barrier Damage Blocked', 'Projected Barriers Applied',
 'Enemies Slept', 'Sleep Dart Hits',
 'Damage Amplified', 'Meteor Strike Kills',
 'Players Halted', 'Supercharger Assists',
 'Adaptive Shield Uses', 'Air Uptime',
 'Damage - Grappling Claw', 'Damage - Piledriver',
 'Damage Taken - Adaptive Shield', 'Damage Taken - Ball',
 'Damage Taken - Tank', 'Grappling Claw Impacts', 'Piledriver Uses',
 'Shielding - Adaptive Shield',
 'Self-Destruct Kills', 'Accretion Kills', 'Accretion Stuns',
 'Damage - Accretion', 'Damage - Hyperspheres', 'Damage Absorbed',
 'Gravitic Flux Damage Done', 'Gravitic Flux Kills',
 'Hyperspheres Direct Hits', 'Amplification Matrix Assists',
 'Healing - Immortality Field',
 'Immortality Field Deaths Prevented', 'Damage - Deflect',
 'Damage - Dragonblade', 'Damage - Dragonblade Total',
 'Damage - Swift Strike', 'Damage - Swift Strike Dragonblade',
 'Damage Reflected', 'Deflection Kills',
 'Dragonblade Kills', 'Dragonblades', 'Damage - Duplicate',
 'Damage - Focusing Beam', 'Damage - Focusing Beam - Bonus Damage Only',
 'Duplicate Kills',
 'Focusing Beam Dealing Damage Seconds', 'Focusing Beam Kills',
 'Focusing Beam Seconds', 'Sticky Bombs Kills', 'Damage - Discord Orb',
 'Damage - Weapon Charged', 'Discord Orb Time', 'Harmony Orb Time',
 'Healing - Harmony Orb', 'Healing - Transcendence',
 'Transcendence Healing',
 'Bob Gun Damage', 'Bob Kills',
 'Damage - Bob', 'Damage - Bob Charge', 'Damage - Coach Gun',
 'Damage - Dynamite', 'Dynamite Kills',
 'Scoped Critical Hits', 'Damage - Deadeye', 'Damage - Flashbang',
 'Deadeye Kills', 'Fan the Hammer Kills',
 'Damage - Minefield', 'Grappling Claw Kills', 'Minefield Kills',
 'Piledriver Kills', 'Infra-sight Uptime', 'Damage - Call Mech',
 'Scoped Critical Hit Kills', 'Damage - Weapon Recon',
 'Damage - Weapon Sentry', 'Damage - Weapon Tank', 'Recon Kills',
 'Sentry Kills', 'Barrage Kills', 'Damage - Barrage',
 'Rocket Barrages', 'Rocket Direct Hits',
 'of Rockets Fired', 'Damage - Sentry Turret', 'Photon Projector Kills',
 'Primary Fire Hits Hits - Level',
 'Secondary Direct Hits', 'Sentry Turret Kills', 'Healing - Weapon Valkyrie',
 'Players Resurrected', 'Players Saved',
 'Biotic Field Healing Done', 'Biotic Fields Deployed',
 'Damage - Helix Rockets', 'Damage - Tactical Visor', 'Helix Rocket Kills',
 'Tactical Visor Kills', 'Tactical Visors',
 'Hooks Attempted', 'Turrets Destroyed', 'Blaster Kills',
 'Damage - Weapon Pistol', 'Damage - Molten Core',
 'Molten Core Kills', 'Turret Damage', 'Turret Kills',
 'Coach Gun Kills', 'Damage - Venom Mine', 'Concussion Mine Kills',
 'Damage - Concussion Mine', 'Frag Launcher Direct Hits',
 'Damage - Steel Trap', 'Enemies Trapped', 'Overload Kills',
 'Damage - Death Blossom', 'Death Blossom Kills',
 'Death Blossoms', 'Venom Mine Kills', 'Damage - RIP-Tire',
 'Damage - Total Mayhem', 'RIP-Tire Kills',
 'Damage - Weapon Hammer', 'Hammer Kills', 'Damage - Chain Hook',
 'Damage - Whole Hog', 'Enemies Hooked',
 'Whole Hog Kills', 'Tank Kills',
 'Total Mayhem Kills']

for s in stats_to_care:
 print("""
 <ng-container matColumnDef="%s">
  <th mat-header-cell *matHeaderCellDef> %s </th>
  <td mat-cell *matCellDef="let row"> {{row.%s}}} </td>
 </ng-container>
 """ % (camelize(s), s, camelize(s)))

frame = frame[frame['Stat'].isin(stats_to_care)].drop_duplicates()
opponents = frame[['Match Id', 'Map Name', 'Team Name', 'Classification']].drop_duplicates()
opponents.columns = ['Match Id', 'Map Name', 'Opponent Team Name', 'Opponent Classification']
frame = frame.merge(opponents, on=['Match Id', 'Map Name'])
frame = frame[frame['Team Name'] != frame['Opponent Team Name']]

frame.to_csv('./out/hero_data_2022.csv', index=False)
frame[['Stat']].drop_duplicates().to_csv('./out/stats.csv', index=False)


