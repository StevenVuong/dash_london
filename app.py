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

dfs = pd.read_csv('./data/gcse-results.csv')
slider_dict={0:"2016-17", 1:"2017-18", 2:"2018-19"}
# ------------------------------------------------------------------------------
# App layout

app = dash.Dash()

app.layout = html.Div([

    html.Label("Select Year"),
    dcc.Slider(id="slider_slct_year",
        min=0,
        max=2,
        step=None,
        marks={
            0:"2016-17",
            1:"2017-18",
            2:"2018-19"
        },
        value=0
        ),
    
    html.Label("Filter by Gender"),
    dcc.RadioItems(id="slct_gender",
                options=[
                    {'label': 'All', 'value': 'all'},
                    {'label': 'Males', 'value': 'male'},
                    {'label': 'Females', 'value': 'female'}],
                value='all'
                ),

    html.Div(id='output_container', children=[]),

    html.Br(),
    dcc.Graph(id="results_map", figure={})
])
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

@app.callback(
    Output(component_id='results_map', component_property='figure'),
    [Input(component_id='slider_slct_year', component_property='value'),
    Input(component_id='slct_gender', component_property='value')]
)
def update_graph(option_slctd_year, option_slctd_gender):

    gjff = gjf.copy()
    dff = dfs.copy()
    option_slctd_year = slider_dict[option_slctd_year]

    option_slctd_year = f"{option_slctd_year}-{option_slctd_gender}"
    dff['Percentage'] = dff[option_slctd_year]
    #dff[option_slctd] = dff['Percentage (%)']

    fig = px.choropleth(dff, geojson=gjff, color="Percentage",
                        locations="Area", featureidkey="properties.name",
                        title=f"Percentage of {option_slctd_gender} Pupils that achieved strong 9 to 5 pass grade in {option_slctd_year}",
                        center={'lat':51.5074, 'lon':0.1277},
                        color_continuous_scale="Viridis",
                        hover_name="Area",
                        hover_data={
                            'Area':False,
                            option_slctd_year:False
                        }
                    )
    fig.update_geos(showcountries=False, 
                    showcoastlines=False, showland=False, fitbounds="locations")
    fig.update_layout(hovermode="x")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
