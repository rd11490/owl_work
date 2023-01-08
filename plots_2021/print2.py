import pandas as pd
import numpy as np
from re import split



# pd.set_option('display.max_columns', 500)
# pd.set_option('display.max_rows', 200)
# pd.set_option('display.width', 1000)
#
# frame = pd.read_csv('./out/hero_data_2022.csv')
#
# data = frame[['Player', 'Hero', 'Stat', 'Amount']].groupby(
#             by=['Player', 'Hero', 'Stat']).sum().reset_index()
# data = data.groupby(by=['Player', 'Hero', 'Stat'])['Amount'].sum().unstack('Stat').reset_index().fillna(0.0)
# print(data)


test = [1, 2, 3, 4, 5]
print(test[0:2])