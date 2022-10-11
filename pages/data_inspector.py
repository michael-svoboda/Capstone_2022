from datetime import date
import dash
from numpy import double
from sqlalchemy import true
dash.register_page(__name__, path="/data_inspector")
from dash import Dash,dash_table, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

import data

#df = px.data.medals_wide(indexed=True)

oil_prod_data = pd.read_csv("./data/oil_prod_data.csv", header = 0)
oil_prod_data["id"] = oil_prod_data['Unique Well ID']
unique_well_ids = oil_prod_data['Unique Well ID'].unique().tolist()
unique_section_ids = oil_prod_data['Section'].unique().tolist()

#print(oil_prod_data.columns)
#print(oil_prod_data['Decade'].to_list)



'''
        dcc.Dropdown(
            id = "uwi_filter_dropdown",
            options=[{"label": uwi, "value": uwi,} for uwi in unique_well_ids],
            placeholder = "--- Filter on UWI ---",
            multi = True,
            value = unique_well_ids,
        ),'''

layout = html.Div(
    children = [
        

        dcc.Dropdown(
            id="dropdown",
            options = [{"label": x, "value": x} for x in unique_section_ids],
            value = unique_section_ids[28:],
            multi = True,
            #labelStyle={'display': 'inline-block'}
        ),
        #dcc.Graph(id="Data Inspector"),
        html.Br(),
        html.Br(),
        dcc.Graph(id='line-chart'),
    ]
)
'''


        dash_table.DataTable(
            id='datatable-interactivity',
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
                if i == "iso_alpha3" or i == "year" or i == "id"
                else {"name": i, "id": i, "deletable": True, "selectable": True}
                for i in oil_prod_data.columns
            ],
            data=oil_prod_data.to_dict('records'),  # the contents of the table
            editable=True,              # allow editing of data inside all cells
            filter_action="native",     # allow filtering of data by user ('native') or not ('none')
            sort_action="native",       # enables data to be sorted per-column by user or not ('none')
            sort_mode="single",         # sort across 'multi' or 'single' columns
            column_selectable="multi",  # allow users to select 'multi' or 'single' columns
            row_selectable="multi",     # allow users to select 'multi' or 'single' rows
            row_deletable=True,         # choose if user can delete a row (True) or not (False)
            selected_columns=[],        # ids of columns that user selects
            selected_rows=[],           # indices of rows that user selects
            page_action="native",       # all data is passed to the table up-front or not ('none')
            page_current=0,             # page number that user is on
            page_size=0,                # number of rows visible per page
            style_cell={                # ensure adequate header width when text is shorter than cell's text
                'minWidth': 95, 'maxWidth': 95, 'width': 95
        }


        ),
'''

@callback(
    Output("line-chart", "figure"), 
    [Input("dropdown", "value")])

def update_line_chart(sections):
    sorted_df = oil_prod_data.sort_values(by= ["Unique Well ID", "Date"]).reset_index(drop=True)
    mask = sorted_df['Section'].isin(sections)
    
    fig = px.scatter(sorted_df[mask], 
        x="Date", y="PRD Calndr-Day Avg BOE Bbl", color='Unique Well ID')
    #fig.update_traces(mode="markers+lines", line_shape="vh")
    return fig

'''
def update_bar (all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
                order_of_rows_indices, order_of_rows_names, actvc_cell, slctd_cell):

    dff = pd.DataFrame(all_rows_data)

    colors = ['#7FDBFF' if i in slctd_row_indices else '#0074D9'
              for i in range(len(dff))]

    return [
        dcc.Graph(id = 'bar-chart',
        figure = px.scatter(
            data_frame = dff,
            x = "Date",
            y = "PRD Calndr-Day Avg BOE Bbl",
            labels = {'Date' : 'Avg BOE'},
            color = 'Unique Well ID'
        ).update_layout(showlegend = False, xaxis = {'categoryorder': 'total ascending'})
        .update_traces(hovertemplate = "<b>%{y}%</b><extra></extra>")
        )]

'''



