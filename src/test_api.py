import requests, json
from pprint import pprint
import pandas as pd

pd.set_option('display.max_columns', None)

base_url = 'https://fantasy.premierleague.com/api/'
r = requests.get(base_url + 'bootstrap-static/').json()
#pprint(r, indent=2, depth=1, compact=True)

players = pd.json_normalize(r['elements'])
pprint(players[0])