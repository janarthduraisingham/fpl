import pandas as pd
from pyprojroot import here
import seaborn as sns
import matplotlib.pyplot as plt
import json
from fpl.player_data import players, positions

def points_ts(pid):
    #print("ewmac commencing...")

    with open(here("data/element_summary/element_summary_"+str(pid)+".json")) as f:
        data = json.load(f)

    df = pd.json_normalize(data['history'])[
        ['element', 'total_points', 'round']
    ]

    # Join names, teams, positions
    names = players()[['PID', 'first_name', 'second_name', 'element_type']]

    df = pd.merge(
        left = df,
        right = names,
        left_on = "element",
        right_on = "PID"
    ).drop(columns=['PID']).merge(
        positions()[['id', 'singular_name']],
            left_on='element_type',
            right_on='id').rename(
        columns={'round':'GW',
                 "singular_name":"position_name"}
            )

    ax = sns.lineplot(data=df, x='GW', y='total_points')
    plot = ax.figure
    plt.close(plot)

    result = {'df':df,
              'plot':plot}
    return(result)

def ewmac_ts(pid, short_alpha=0.5, long_alpha=0.25):
    df = points_ts(pid)['df']
    df['ewma_'+str(short_alpha)] = df['total_points'].ewm(alpha=short_alpha).mean()
    df['ewma_'+str(long_alpha)] = df['total_points'].ewm(alpha=long_alpha).mean()

    df['ewmac_'+str(short_alpha)+'_'+str(long_alpha)] = df['ewma_'+str(short_alpha)] - df['ewma_'+str(long_alpha)]
    df['sma_4'] = df['total_points'].rolling(4).mean()


    df_tidy = df[['GW', 'total_points', 'ewma_0.5', 'ewma_0.25', 'ewmac_0.5_0.25', 'sma_4']].melt(
            id_vars = 'GW',
            var_name= 'statistic',
            value_name= 'value'
        )
    ax = sns.lineplot(data=df_tidy, x='GW', y='value', hue='statistic')
    plot = ax.figure
    plt.close(plot)


    result = {'df':df,
              'plot':plot}

    return(result)


def ewmac_all(gw):

    rows = []

    for pid in players()['PID']:
        #print(pid)
        df = ewmac_ts(pid=pid,
                      short_alpha=0.5,
                      long_alpha=0.25)['df']
        df = df[df['GW']==gw]
        rows.append(df)

    df = pd.concat(rows, ignore_index=True).sort_values(
        by=['sma_4', 'ewmac_0.5_0.25'],
        ascending=[False, False]
    )[
        ['first_name', 'second_name', 'position_name', 'sma_4', 'ewmac_0.5_0.25']
    ]

    return(df)

if __name__ == '__main__':
    #print(ewmac_df'])
    print(ewmac_all(gw=5))
