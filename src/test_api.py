import requests, json
from pprint import pprint
import pandas as pd

pd.set_option('display.max_columns', None)

base_url = 'https://fantasy.premierleague.com/api/'
#r = requests.get(base_url + 'bootstrap-static/').json()
#pprint(r, indent=2, depth=1, compact=True)

#with open('bootstrap-static.json', 'w') as f:
#    json.dump(r, f)

with open('bootstrap-static.json') as f:
    r = json.load(f)

players = pd.json_normalize(r['elements']).rename(
    columns={'id':'PID'}
)
pprint(players[['PID', 'web_name', 'team', 'element_type']])

print(players.columns)

teams = pd.json_normalize(r['teams'])

positions = pd.json_normalize(r['element_types'])

df = pd.merge(
    left = players,
    right = teams,
    left_on = 'team',
    right_on = 'id'
)

df = df.merge(
    positions,
    left_on = 'element_type',
    right_on = 'id'
).rename(
    columns={
        'name':'team_name',
        'singular_name':'position_name'
    }
)

print(df[['PID', 'first_name', 'second_name', 'team_name', 'position_name']].head(20))

# For each gameweek, get all player data: https://fantasy.premierleague.com/api/event/{GID}/
# For each player, get gameweeek history: https://fantasy.premierleague.com/api/element-summary/{PID}
pids = df['PID']

for pid in pids:
    print(pid)
    pid_gameweek_history = requests.get(base_url + 'element-summary/' + str(pids[0]) + '/').json()

    with open('data/element_summary/element_summary_' + str(pid) + '.json', 'w') as f:
        json.dump(pid_gameweek_history, f)