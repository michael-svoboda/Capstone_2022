import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objs.layout import YAxis,XAxis,Margin


def identify_log_tracks(logs):

    '''
    This function is going to attempt to identify the tracks that the past logs belong to. Split the original list
    into separate lists that then get passed back.

    1: [GR (api), CALI (mm), SP (mV)]
    2: [AC (us/ft), DEN (g/cm^3), PE (b/e), CNL (%)]
    3: [RMSF (ohm * m), RLLS (ohm * m), RLLD (ohm * m)]
    4: [RLLD (ohm * m), AC (us / ft)]

    Categories of units:
        [api, mm, mV, us/ft, g/cm^3, b/e, %, ohm*m]
    '''

    curves_df = pd.read_csv('data/databases/Curves.csv')
    

    # logs will be passed into this function, first filter down the Curves df
    # then we will look at the units column and get a unique list of the units for each log
    # then check the equivalent units for that log, and plot on corresponding track
    # if log == RLLD or AC, then also send to the track 4 list




    track = {
        '1' : [],
        '2' : [],
        '3' : [],
        '4' : []
    }

    # send back track dictionary, and then pass each list of logs into corresponding track graphing function

    return track

def add_track_1_curves(fig, df, logs, low, high, well_names):
    
    # we need to determine which logs are selected.
    # Then based on the units we will plot onto one of the tracks and axis
    # For now we will just hard code the names for testing

    # On track_1 we want the GR, CALI, SP (3 axis)

    # we will save the parameters of the graph into a dict and find the corresponding elements from there
    track_1_params = {
        'GR' : ['x1'],
        'GRD' : ['x1'],
        'GRP' : ['x1'],
        'GRS' : ['x1'],
        'GRZ' : ['x1'],
        'CALI': ['x2'],
        'SP':['x3']
    }

    for well in well_names:

        for log in logs:

            print("THE LOGS: ", logs)

            if log in track_1_params:

                print("ENTERED IF")
                print(log)
                params = track_1_params[log]

                correction_factor = 1

                axis = 'x1'

                if log == 'CALI':
                    correction_factor = 10
                    axis = 'x2'
                
                # creating a mask by applying filters to the dataframe
                mask = (df['DEPT'] > low) & (df['DEPT'] < high) & df['UWI'].isin([well])

                print(df[mask][log])
                print("AXIS: ", params[0])

                fig.add_trace(
                go.Scatter(x = df[mask][log]/correction_factor, y = df[mask]["DEPT"], mode='lines', name= log + "_" + well, xaxis = params[0])

                )


    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        legend=dict(
            x=0.27,
            y=0.89,),
        xaxis=dict(range=[0, 150]),
        xaxis1=dict(range=[0, 150]),
        xaxis2=dict(range=[10, 40]),
        xaxis3=dict(range=[-150, 150]),
        yaxis=dict(range=[low, high]),
        #xaxis3=dict(range=[-80, 80]),
        width=580,
        height=2000,
        )

    #fig.show()

    return fig



def add_track_2_curves(fig, df, logs, low, high, well_names):
    
    # we need to determine which logs are selected.
    # Then based on the units we will plot onto one of the tracks and axis
    # For now we will just hard code the names for testing

    # On track_1 we want the GR, CALI, SP (3 axis)

    # we will save the parameters of the graph into a dict and find the corresponding elements from there
    track_1_params = {
        'ILD':['x'],
        'ILM':['x'],
        'SFL':['x'],
        'LL8':['x'],
        'AT20':['x'],
        'AT30':['x'],
        'AT90':['x'],
        'IDPH':['x'],
        'IMPH':['x'],
        'LN64':['x'],
        'SN16':['x']
    }

    for well in well_names:

        for log in logs:

            print("THE LOGS: ", logs)

            if log in track_1_params:

                print("ENTERED IF")
                print(log)
                params = track_1_params[log]

                correction_factor = 1

                axis = 'x1'

                if log == 'CALI':
                    correction_factor = 10
                    axis = 'x2'
                
                # creating a mask by applying filters to the dataframe
                mask = (df['DEPT'] > low) & (df['DEPT'] < high) & df['UWI'].isin([well])

                print(df[mask][log])
                print("AXIS: ", params[0])

                fig.add_trace(
                go.Scatter(x = df[mask][log]/correction_factor, y = df[mask]["DEPT"], mode='lines', name= log + "_" + well, xaxis = params[0])

                )


    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(type="log")
    fig.update_layout(
        legend=dict(
            x=0.27,
            y=0.89,),
        xaxis=dict(range=[-0.69897,3.30102]),
        yaxis=dict(range=[low, high]),
        #xaxis3=dict(range=[-80, 80]),
        width=580,
        height=2000,
        )

    #fig.show()

    return fig        


def add_track_3_curves(fig, df, logs, low, high, well_names):
    
    # we need to determine which logs are selected.
    # Then based on the units we will plot onto one of the tracks and axis
    # For now we will just hard code the names for testing

    # On track_1 we want the GR, CALI, SP (3 axis)

    # we will save the parameters of the graph into a dict and find the corresponding elements from there
    track_3_params = {
        'DPHI:1':['x'],
        'DPHI:2':['x'],
        'NPHI:1':['x'],
        'NPHI:2':['x'],
        'POS':['x'],
        'POS':['x'],
        'POL':['x']
    }

    for well in well_names:

        for log in logs:

            print("THE LOGS: ", logs)

            if log in track_3_params:

                print("ENTERED IF")
                print(log)
                params = track_3_params[log]

                correction_factor = 1

                axis = 'x1'

                if log == 'CALI':
                    correction_factor = 10
                    axis = 'x2'
                
                # creating a mask by applying filters to the dataframe
                mask = (df['DEPT'] > low) & (df['DEPT'] < high) & df['UWI'].isin([well])

                print(df[mask][log])
                print("AXIS: ", params[0])

                fig.add_trace(
                go.Scatter(x = df[mask][log]/correction_factor, y = df[mask]["DEPT"], mode='lines', name= log + "_" + well, xaxis = params[0])

                )


    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        legend=dict(
            x=0.27,
            y=0.89,),
        xaxis=dict(range=[-15,45]),
        yaxis=dict(range=[low, high]),
        #xaxis3=dict(range=[-80, 80]),
        width=580,
        height=2000,
        )

    #fig.show()

    return fig     