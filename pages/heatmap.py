import dash
dash.register_page(__name__, path="/heatmap")
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import data

df = px.data.gapminder()
all_continents = df.continent.unique()


layout = html.Div([
    dcc.Checklist(
        id="checklist1",
        options=[{"label": x, "value": x} 
                 for x in all_continents],
        value=all_continents[3:],
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="line-chart1"),
])


@callback(
    Output("line-chart1", "figure"), 
    [Input("checklist1", "value")])
def update_line_chart(continents):
    mask = df.continent.isin(continents)
    fig = px.line(df[mask], 
        x="year", y="lifeExp", color='country')
    return fig