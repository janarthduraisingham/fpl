import pandas as pd
import matplotlib.pyplot as plt
from fpl.ewmac import *
from fpl.player_data import teams

def get_correlation(pid1, pid2, gw):

    # Get player points timeseries
    #teams_df = teams()[['id', 'name']]
    #df1 = points_ts(pid1)['df']#.merge(
        #teams_df,
        #left_on = 'team',
        #right_on = 'id'
    #)[['GW', 'PID', 'second_name', 'total_points', 'element_type', 'team']]

    with open(here("data/element_summary/element_summary_"+str(pid1)+".json")) as f:
            data = json.load(f)
    
    df1 = pd.json_normalize(data['history'])[
        ['element', 'total_points', 'round']
    ].rename(
          columns={'round':'GW'}
    )

    #df1 = df1[df1['GW']<=gw][['GW', 'PID', 'second_name', 'total_points', 'element_type', 'team']]

    with open(here("data/element_summary/element_summary_"+str(pid2)+".json")) as f:
                data = json.load(f)
        
    df2 = pd.json_normalize(data['history'])[
        ['element', 'total_points', 'round']
    ].rename(
          columns={'round':'GW'}
    )

    df1 = df1[df1['GW']<=gw]#[['GW', 'PID', 'second_name', 'total_points', 'element_type', 'team']]

    #df2 = points_ts(pid2)['df']#.merge(
    #        teams_df,
    #        left_on = 'team',
    #        right_on = 'id'
    #    )
    
    df2 = df2[df2['GW']<=gw]#[['GW', 'PID', 'second_name', 'total_points', 'element_type', 'team']]

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


def plot_all_correlations(gw,
                          same_team = 0,
                          same_position = 0):

      filepath = here("output/correlations_same_team_"+str(same_team)+"_same_position_"+str(same_position)+".png")

      df = pd.read_csv(here("data/correlations/gw"+str(gw)+"/all_correlations_gw_"+str(gw)+".csv"))
      df = df[df['PID_x']!=df['PID_y']]

      if same_team == 1:
              df = df[df['team_x'] == df['team_y']]

      ax = sns.histplot(data=df,
                          x="correlation",
                          stat='density')
      plot = ax.figure
      plot.savefig(filepath)
      #plt.show()
      plt.close(plot)

      return({'plot':plot,
              'df' : df})


def plot_multiple_correlations(same_team_1 = 0, same_position_1 = 0, label_1 = 'all correlations',
                               same_team_2 = 1, same_position_2 = 0, label_2 = 'intra-team correlations'):

      df1 = plot_all_correlations(gw=10, same_team = same_team_1, same_position = same_position_1)['df']
      df2 = plot_all_correlations(gw=10, same_team = same_team_2, same_position = same_position_2)['df']

      fig, ax = plt.subplots(figsize=(8, 5))

      sns.histplot(data=df1, stat='density', x="correlation", ax=ax, color="tab:blue", alpha=0.5, label=label_1)
      sns.histplot(data=df2, stat='density', x="correlation", ax=ax, color="tab:orange", alpha=0.5, label=label_2)

      ax.legend()
      plt.show()
      plt.close(fig)

if __name__ == '__main__':
    print("running...")
    plot_multiple_correlations()
    #plot_all_correlations(gw=10)
    print("complete")
