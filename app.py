import json
import pandas as pd
import plotly.express as px
import geojson

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
with open('./data/london_boroughs.json') as f:
    gjf = geojson.load(f)

dfs = pd.read_excel('./data/gcse-results.xlsx', sheet_name="strong_9_5_pass")
# ------------------------------------------------------------------------------
# App layout

app = dash.Dash()

app.layout = html.Div([

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2016-17", "value": "2016-17"},
                     {"label": "2017-18", "value": "2017-18"},
                     {"label": "2018-19", "value": "2018-19"}],
                 multi=False,
                 value="2016-17",
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),

    html.Br(),
    dcc.Graph(id="results_map", figure={})
])
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

@app.callback(
    Output(component_id='results_map', component_property='figure'),
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):

    gjff = gjf.copy()
    dff = dfs.copy()

    dff['Percentage'] = dff[option_slctd]
    #dff[option_slctd] = dff['Percentage (%)']

    fig = px.choropleth(dff, geojson=gjff, color="Percentage",
                        locations="Area", featureidkey="properties.name",
                        title=f"Percentage of Pupils that achieved strong 9 to 5 pass grade in {option_slctd}",
                        center={'lat':51.5074, 'lon':0.1277},
                        color_continuous_scale="Blues",
                        hover_name="Area",
                        hover_data={
                            'Area':False,
                            option_slctd:False
                        }
                    )
    fig.update_geos(showcountries=False, 
                    showcoastlines=False, showland=False, fitbounds="locations")
    fig.update_layout(hovermode="x")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
