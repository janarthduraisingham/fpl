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
    corr = x.corr(y)

    return(float(corr))


def all_correlations(pid=1, gw=10):

    players_list = players()['PID']

    correlations = [get_correlation(pid1=1, pid2=x, gw=gw) for x in players_list]

    pd.Series(correlations).to_csv("data/correlations/gw"+str(gw)+"/all_correlations_pid_"+str(pid)+"_gw_"+str(gw)+".csv",
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
    for pid in players()['PID']:
        print(pid)
        all_correlations(pid=pid, gw=10)
    #x = pd.read_csv("data/correlations/gw10/all_correlations_pid_1_gw_10.csv")
    #print(x)
    print("complete")
