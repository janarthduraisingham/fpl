import pandas as pd
import matplotlib.pyplot as plt
from fpl.ewmac import *
from fpl.player_data import teams

def get_correlation(pid1, pid2, gw):

    # Get player points timeseries
    teams_df = teams()[['id', 'name']]
    df1 = points_ts(pid1)['df'].merge(
        teams_df,
        left_on = 'team',
        right_on = 'id'
    )[['GW', 'PID', 'second_name', 'total_points', 'element_type', 'team']]

    df1 = df1[df1['GW']<=gw]

    df2 = points_ts(pid2)['df'].merge(
            teams_df,
            left_on = 'team',
            right_on = 'id'
        )[['GW', 'PID', 'second_name', 'total_points', 'element_type', 'team']]
    
    df2 = df2[df2['GW']<=gw]

    x = df1.set_index("GW")["total_points"].fillna(0)
    y = df2.set_index("GW")["total_points"].fillna(0)
    corr = float(x.corr(y))

    return({'pid1':pid1,
            'pid2':pid2,
            'correlation':corr})

def all_correlations(gw):

    players_list = players()['PID']

    rows = [get_correlation(pid1, pid2, gw=gw)
            for pid1 in players_list
            for pid2 in players_list]

    df = pd.DataFrame(rows).merge(
        players()[['PID', 'second_name', 'team', 'element_type']],
        left_on = 'pid1',
        right_on = 'PID'
    ).rename(columns={"second_name":"player_1"}).merge(
        players()[['PID', 'second_name', 'team', 'element_type']],
        left_on = 'pid2',
        right_on = 'PID'
    ).rename(columns={"second_name":'player_2'})

    df.to_csv("data/correlations/gw"+str(gw)+"/all_correlations_gw_"+str(gw)+".csv")

    return(df)

def all_correlation(pid=1, gw=10, folder="all"):

    players_list = players()['PID'][0:10]

    correlations = [get_correlation(pid1=1, pid2=x, gw=gw) for x in players_list]

    pd.Series(correlations).to_csv("data/correlations/gw"+str(gw)+"/"+folder+"/all_correlations_pid_"+str(pid)+"_gw_"+str(gw)+".csv",
                                   index=None,
                                   header="correlations")

    #plt.hist(pd.Series(correlations), bins=10, edgecolor="black")
    #plt.xlabel("Correlation")
    #plt.ylabel("Count")
    #plt.title("Distribution of correlations")
    #plt.show()

    return(plt)

if __name__ == '__main__':
    print("running...")
    #for pid in players()['PID']:
    #    print(pid)
    #    all_correlations(pid=pid, gw=10)
    #x = pd.read_csv("data/correlations/gw10/all_correlations_pid_1_gw_10.csv")
    #print(x)
    #print(get_correlation(pid1=1, pid2=20, gw=10))
    print(all_correlations(gw=10))
    print("complete")
