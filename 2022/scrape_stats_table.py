import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

url = 'https://overwatchleague.com/en-us/stats/2022/owl2-2022-regular'

resp = requests.get(url)

txt = resp.text
soup = BeautifulSoup(txt, 'html.parser')


source_script = soup.find(id="__NEXT_DATA__")
json_string = source_script.get_text()

resp_data = json.loads(json_string)
blocks = resp_data['props']['pageProps']['blocks']
for b in blocks:
    if 'statistics' in b.keys():
        player_stats = b['statistics']['stats']
        break

frame = pd.DataFrame(player_stats)

frame.to_csv('2022_player_data.csv', index=False)
