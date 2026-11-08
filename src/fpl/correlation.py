import pandas as pd
import matplotlib.pyplot as plt
from fpl.ewmac import *
from fpl.player_data import teams

def get_correlations(pid):

    # Get player points timeseries
    teams_df = teams()[['id', 'name']]
    df = points_ts(pid)['df'].merge(
        teams_df,
        left_on = 'team',
        right_on = 'id'
    )[['PID', 'second_name', 'total_points', 'element_type', 'team']] 

    return(df)


if __name__ == '__main__':
    print("running...")
    #print(points_ts(pid=1)['df'])
    print(get_correlations(pid=1))
    print("complete")
