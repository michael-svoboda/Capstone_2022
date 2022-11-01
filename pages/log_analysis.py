import dash
from dash import no_update
import dash_bootstrap_components as dbc
from matplotlib.axis import XAxis
dash.register_page(__name__, path="/")
from dash import Dash, dcc, html, Input, Output, State, callback
from plotly.graph_objs.layout import YAxis,XAxis,Margin
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import copy
#import data

from dash import Dash, dcc, html, Input, Output
import plotly.express as px

from pages import graphing

def get_unique_well_list(df) :
    unique_UWI_list = df['UWI'].unique().tolist()
    return unique_UWI_list

df = pd.read_csv('../data/databases/curves_values.csv') # replace with your own data source
unique_UWI_list = get_unique_well_list(df)
log_list = df.columns.to_list()

# Lets try to edit the unique well list based on the inputs from other filters.

controls = dbc.Card(
    [
        html.P("Select UWI:"),
        dcc.Dropdown(
                            id="well_dropdown",
                            options = [{"label": x, "value": x} for x in get_unique_well_list(df)],
                            value = '100090306119W500',
                            multi = True,
                            #labelStyle={'display': 'inline-block'}
                        ),
        dcc.Dropdown(
                            id="log_dropdown",
                            options = [{"label": x, "value": x} for x in log_list],
                            value = ['GR'],
                            multi = True,
                            #labelStyle={'display': 'inline-block'}
                        ),
        #html.Button('Graph', id='graph_button', n_clicks=0),
        html.P("Filter by DEPTH:"),
        dcc.RangeSlider(
                        id='range-slider',
                        min=2500, max=3500, step=25,
                        marks={2500: '2500',2600: '2600', 2700: '2700', 2800: '2800', 2900: '2900', 3000: '3000', 3100: '3100',3200: '3200',3300: '3300',3400: '3400', 3500:'3500'},
                        value=[3000, 3400],
                        vertical= True
                    ),

    ],
)

layout = dbc.Container([

    html.H4('LOGGING ANALYSIS'),
    
    dbc.Row([
        dbc.Col(
                        controls,
                        width = 2,
                    ),
        dbc.Card([
            dbc.Row([
                        dbc.Col(
                            dcc.Graph(
                                id="track_1",
                                ),
                            width = 4,
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id="track_2",
                                ),
                            width = 4,
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id="track_3",
                                ),
                            width = 4,
                        )

                ],
            ),
        ],
        style={"width": "95rem"},
        ),
    ])

],
fluid= True
)

#


@callback(
    Output("track_1", "figure"),
    Output("track_2", "figure"),
    Output("track_3", "figure"),
    Input("range-slider", "value"),
    Input("well_dropdown", "value"),
    State("log_dropdown", "value")
    )

def update_graph(slider_range, well_names, logs):

    print('LOGGERS: ', logs)
    low, high = slider_range
    df = pd.read_csv('../data/databases/curves_values.csv')
    #print(well_names)

    if not(type(well_names) is list):
        well_names = [well_names]

    track_1 = make_subplots()
    track_2 = make_subplots()
    track_3 = make_subplots()

    # Track #1 Layout
    layout1 = go.Layout(
        title="Track 1",
        
        xaxis1=  XAxis(
            title="Gamma (api)",
            side= 'top',
            #overlaying= 'x',
            position = 1
        ),

        xaxis2 =  XAxis(
            title="Caliper (cm)",
            overlaying= 'x1', 
            side= 'top',
            position = 0.90
        ),

        xaxis3 =  XAxis(
            title="SP (mV)",
            overlaying= 'x1', 
            side= 'top',
            position = 0.95
        ),

        yaxis=dict(
            title="Depth (mKB)"
        ),
    )

    # Track #2 Layout
    layout2 = go.Layout(
        title="Track 2",
        
        xaxis1=  XAxis(
            title="Resisitivity (ohmm)",
            side= 'top',
            #overlaying= 'x',
            position = 1
        ),

        yaxis=dict(
            title="Depth (mKB)"
        ),
    )


    # Track #3 Layout
    layout3 = go.Layout(
        title="Track 3",
        
        xaxis1=  XAxis(
            title="Resisitivity (ohmm)",
            side= 'top',
            #overlaying= 'x',
            position = 1
        ),

        yaxis=dict(
            title="Depth (mKB)"
        ),
    )
    # Setting fig to use the track 1 layout, then passing into the add curves function
    fig1 = go.Figure(layout=layout1)
    fig2 = go.Figure(layout=layout2)
    fig3 = go.Figure(layout=layout1)

    track_1 = graphing.add_track_1_curves(fig1, df, logs, low, high, well_names)
    track_2 = graphing.add_track_2_curves(fig2, df, logs, low, high, well_names)
    track_3 = graphing.add_track_3_curves(fig3, df, logs, low, high, well_names)

    return track_1, track_2, track_3

@callback(
    Output("well_dropdown", "options"),
    Input("log_dropdown", "value")
    )

def filter_wells(log_names):

    final_UWI_list = []

    if not not log_names:

        print('ENTERED')
        print('Log names: ', log_names)

        if not(type(log_names) is list):
            log_names = [log_names, 'UWI']
        else:
            log_names = log_names + ['UWI']

        # we need to filter down the df to show wells that only include the selected logs
        df = pd.read_csv('../data/databases/curves_values.csv')
        df_filtered = df.loc[:, df.columns.isin(log_names)]

        #print('SERIES', df_filtered['GRS'].isnull().values.tolist())
        #print(type(df_filtered['GRS'].isnull().values.tolist()))

        # creating the masks to overlay the 

        print(df_filtered.columns.to_list())
        col_list = df_filtered.columns.to_list()
        col_list.remove('UWI')
        print('COLUMN LIST: ', col_list)

        masks = [df_filtered[col].isnull().values.tolist() for col in col_list]

        

        print('MASKS:', df_filtered.columns.to_list())

        #print('MASKS:', masks)

        # creating a merged mask
        merged_mask = None

        for mask in masks:
            print('Init truths:', sum(mask))
            #print('Init length:', len(mask))
            if not(merged_mask is None):
                merged_mask = [a and b for a, b in zip(merged_mask, mask)]
                print('Modified truths', sum(merged_mask))
                '''np_mask = np.array(mask)
                np_merged_mask = np.array(merged_mask)
                print('merged truths:', np.count_nonzero(np_merged_mask))
                print('mask truths:', np.count_nonzero(np_mask))
                new_merged_mask = np_merged_mask & np_mask
                merged_mask = new_merged_mask.tolist()
                print('Modified truths', sum(merged_mask))
                print('Modified length:', len(merged_mask))'''
            else:
                merged_mask = mask
        
        #print(merged_mask)
        merged_mask = [not elem for elem in merged_mask]

        
        # filtering the df with the merged mask
        df_filtered = df_filtered[merged_mask]
        df_filtered = df_filtered.dropna()

        #df_filtered.to_csv('df_filtered.csv')
        print('exported')
        
        print('filtered')

        unique_UWI_list = get_unique_well_list(df_filtered)
        print('wells : ', unique_UWI_list)

        final_UWI_list = [{"label": x, "value": x} for x in unique_UWI_list]

    else:

        final_UWI_list = [{"label": "No Wells", "value": "No Wells"}]

    return final_UWI_list

    '''return  [
        no_update if not final_UWI_list else final_UWI_list
    ]'''



