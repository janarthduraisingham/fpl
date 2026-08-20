import requests, json
from pprint import pprint
import pandas as pd

pd.set_option('display.max_columns', None)

#base_url = 'https://fantasy.premierleague.com/api/'
#r = requests.get(base_url + 'bootstrap-static/').json()
#pprint(r, indent=2, depth=1, compact=True)

#with open('bootstrap-static.json', 'w') as f:
#    json.dump(r, f)

with open('bootstrap-static.json') as f:
    r = json.load(f)

players = pd.json_normalize(r['elements'])
pprint(players[['id', 'web_name', 'team', 'element_type']])

print(players.columns)

teams = pd.json_normalize(r['teams'])

print(teams.head())