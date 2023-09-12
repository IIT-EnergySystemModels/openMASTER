# Import necessary libraries
import pandas as pd
import os
import sys
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

from modules.energy_sankey_fig import energy_sankey_figure
from modules.energy_barchart_fig import energy_barchart_figure
from modules.energy_pie_chart_fig import energy_pie_chart_figure
from modules.energy_areachart_fig import energy_area_chart_figure
from modules.emissions_areachart_fig import emissions_area_chart_figure

# ======================= #
# PACKAGING RESOURCE PATH #
# ======================= #
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

# === #
# APP #
# === #

# Initialize the app with Bootstrap theme and custom font
external_stylesheets = [dbc.themes.LUX]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

# SCENARIOS DATA PATH
SCENARIOS_DATA_PATH = ".scenarios"
scenarios_folders = [folder for folder in os.listdir(SCENARIOS_DATA_PATH) if "DS_STORE" not in str(folder.upper())] 

# This function loads the data based on the selected scenario
def load_data(scenario):

    # DATA PATH
    DATA_PATH = os.path.join(resource_path("assets/data"))
    SCENARIO_PATH = os.path.join(SCENARIOS_DATA_PATH, scenario)
    # MAPPINGS_DATA_PATH
    MAPPINGS_DATA_PATH = os.path.join(DATA_PATH, "mappings")
    # INPUT_DATA_PATH
    INPUT_DATA_PATH = os.path.join(SCENARIO_PATH, "data/tmp/input")
    # OUTPUT_DATA_PATH
    OUTPUT_DATA_PATH = os.path.join(SCENARIO_PATH, "data/tmp/output")

    return MAPPINGS_DATA_PATH, INPUT_DATA_PATH, OUTPUT_DATA_PATH
#------

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Img(src=resource_path("/assets/images/openMASTER_nobg.png"), height='100px', style={'display': 'block', 'margin': 'auto'}),
                html.H2('Results Visualizer', style={'textAlign': 'center', 'margin': '20px 0px'}),
                html.Label('Choose Scenario'),
                dcc.Dropdown(
                    id='scenario-dropdown',
                    options= [{'label': folder, 'value': folder} for folder in scenarios_folders],
                    value=scenarios_folders[-1]
                ),
                html.Label('Choose Year', style={'marginTop': '20px'}),
                dcc.Input(
                    id='year-input',
                    type='number',
                    min=2020,
                    max=2050,
                    step=5,
                    value=2030,
                ),
                html.Hr(),
                html.Div([
                    html.Label('Choose Second Scenario for Comparison', style={'marginTop': '20px'}),
                    dcc.Dropdown(
                        id='scenario-dropdown2',
                        options= [{'label': folder, 'value': folder} for folder in scenarios_folders],
                        value=scenarios_folders[-1]
                    ),
                    html.Label('Choose Comparison Year', style={'marginTop': '20px'}),
                    dcc.Input(
                        id='comparison-year-input',
                        type='number',
                        min=2020,
                        max=2050,
                        step=5,
                        value=2030,
                    ),
                    html.Hr(),
                    html.Label('Select Graph Type', style={'marginTop': '20px'}),
                    dcc.Dropdown(
                        id='graph-type-dropdown',
                        options=[
                            {'label': 'Energy Sankey', 'value': 'energy_sankey'},
                            {'label': 'Energy Barchart', 'value': 'energy_barchart'},
                            {'label': 'Energy Piechart', 'value': 'energy_piechart'},
                            {'label': 'Energy Areachart', 'value': 'energy_areachart'},
                            {'label': 'Emissions Areachart', 'value': 'emissions_areachart'},
                        ],
                        value='energy_sankey'  # default value
                    ),
                ], id='comparison-dropdown', style={'display': 'none'})  # initially hidden
            ], width=2, style={'padding': '15px', 'backgroundColor': '#f9f9f9', 'borderRight': '0'}),

            dbc.Col([
                dcc.Loading(
                    id="loading",
                    type="default",
                    children=[
                        dcc.Tabs(id='tabs', value='tab-1', children=[
                            dcc.Tab(label='Energy', value='tab-1'),
                            dcc.Tab(label='Emissions', value='tab-2'),
                            dcc.Tab(label='COMPARATOR', value='tab-3'),
                        ]),
                        html.Div(id='tabs-content'),
                        html.Div([
                            dbc.Row([
                                dbc.Col(dcc.Graph(id='graph-energy1', figure={}), md=7),
                                dbc.Col(dcc.Graph(id='graph-energy3', figure={}), md=5),
                            ]),
                            dbc.Row([
                                dbc.Col(dcc.Graph(id='graph-energy4', figure={}), md=6),
                                dbc.Col(dcc.Graph(id='graph-energy2', figure={}), md=6)
                            ])
                        ], id='energy-content', style={'display': 'none'}),
                        html.Div([
                            dbc.Row([
                                dbc.Col(dcc.Graph(id='graph-emissions1', figure={}), md=12)
                            ])
                        ], id='emissions-content', style={'display': 'none'}),
                        html.Div([
                            #html.H3('Comparison'),
                            dbc.Row([
                                dbc.Col(dcc.Graph(id='graph-comparison', figure={})),
                            ], style={'marginBottom': '20px'}),
                            dbc.Row([
                                dbc.Col(dcc.Graph(id='graph-comparison2', figure={})),
                            ], style={'marginBottom': '20px'}),
                        ], id='comparison-content', style={'display': 'none'})
                    ]
                ),
            ], style={'height': '100vh'}, width=10)
        ])
    ], fluid=True)
])

@app.callback(
    Output('tabs-content', 'children'),
    Output('energy-content', 'style'),
    Output('emissions-content', 'style'),
    Output('comparison-content', 'style'),
    Output('comparison-dropdown', 'style'),  # new output
    Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return None, {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}
    elif tab == 'tab-2':
        return None, {'display': 'none'}, {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
    elif tab == 'tab-3':
        return None, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'block'}  # shown when third tab is selected
    

@app.callback(
    Output('graph-comparison', 'figure'),
    Output('graph-comparison2', 'figure'),
    [Input('scenario-dropdown', 'value'),
     Input('scenario-dropdown2', 'value'),
     Input('year-input', 'value'),
     Input('comparison-year-input', 'value'),
     Input('graph-type-dropdown', 'value')])
def update_comparison_graph(scenario1, scenario2, year, comparison_year, graph_type):
    # Generating the data path for each scenario
    MAPPINGS_DATA_PATH1, INPUT_DATA_PATH1, OUTPUT_DATA_PATH1 = load_data(scenario1)
    MAPPINGS_DATA_PATH2, INPUT_DATA_PATH2, OUTPUT_DATA_PATH2 = load_data(scenario2)

    # Plotting the graphs by type and comparison year
    if graph_type == "energy_sankey":
        comparison_fig1 = energy_sankey_figure(year, MAPPINGS_DATA_PATH1, INPUT_DATA_PATH1, OUTPUT_DATA_PATH1, plot_title=scenario1+ " " + str(year) + " Scenario - " + "Energy Flows")
        comparison_fig2 = energy_sankey_figure(comparison_year, MAPPINGS_DATA_PATH2, INPUT_DATA_PATH2, OUTPUT_DATA_PATH2, plot_title=scenario2+ " " + str(comparison_year) + " Scenario - " + "Energy Flows")
    elif graph_type == "energy_barchart":
        comparison_fig1 = energy_barchart_figure(MAPPINGS_DATA_PATH1, INPUT_DATA_PATH1, OUTPUT_DATA_PATH1, title=scenario1+ " Scenario - " + "Primary Energy Consumption")
        comparison_fig2 = energy_barchart_figure(MAPPINGS_DATA_PATH2, INPUT_DATA_PATH2, OUTPUT_DATA_PATH2, title=scenario2+ " Scenario - " + "Primary Energy Consumption")
    elif graph_type == "energy_piechart":
        comparison_fig1 = energy_pie_chart_figure(year, MAPPINGS_DATA_PATH1, INPUT_DATA_PATH1, OUTPUT_DATA_PATH1, title_text=scenario1+ " " + str(year) +" Scenario - " + "Renewable Energy Generation")
        comparison_fig2 = energy_pie_chart_figure(comparison_year, MAPPINGS_DATA_PATH2, INPUT_DATA_PATH2, OUTPUT_DATA_PATH2, title_text=scenario2+  " " + str(comparison_year) + " Scenario - " + "Renewable Energy Generation")
    elif graph_type == "energy_areachart":
        comparison_fig1 = energy_area_chart_figure(MAPPINGS_DATA_PATH1, INPUT_DATA_PATH1, OUTPUT_DATA_PATH1, title=scenario1+ " Scenario - " + "Renewable Energy Generation")
        comparison_fig2 = energy_area_chart_figure(MAPPINGS_DATA_PATH2, INPUT_DATA_PATH2, OUTPUT_DATA_PATH2, title=scenario2+  " Scenario - " + "Renewable Energy Generation")
    elif graph_type == "emissions_areachart":
        comparison_fig1 = emissions_area_chart_figure(MAPPINGS_DATA_PATH1, INPUT_DATA_PATH1, OUTPUT_DATA_PATH1, title=scenario1+ " Scenario - " + "Sector-wise CO2 Emission Over Time")
        comparison_fig2 = emissions_area_chart_figure(MAPPINGS_DATA_PATH2, INPUT_DATA_PATH2, OUTPUT_DATA_PATH2, title=scenario2+ " Scenario - " + "Sector-wise CO2 Emission Over Time")
    else:
        comparison_fig1 = None
        comparison_fig2 = None

    # Resizing the figures
    comparison_fig1.update_layout(autosize=True)
    comparison_fig2.update_layout(autosize=True)
    
    return comparison_fig1, comparison_fig2

    
@app.callback(
    [Output('graph-energy1', 'figure'),
     Output('graph-energy2', 'figure'),
     Output('graph-energy3', 'figure'),
     Output('graph-energy4', 'figure'),
     Output('graph-emissions1', 'figure')],
    [Input('scenario-dropdown', 'value'),
     Input('year-input', 'value')])
def update_graphs(scenario, year):

    # Data Paths
    MAPPINGS_DATA_PATH, INPUT_DATA_PATH, OUTPUT_DATA_PATH = load_data(scenario)

    # Energy Sankey
    energy_sankey_fig = energy_sankey_figure(year, MAPPINGS_DATA_PATH, INPUT_DATA_PATH, OUTPUT_DATA_PATH)
    # Energy Barchart 
    energy_barchart_fig = energy_barchart_figure(MAPPINGS_DATA_PATH, INPUT_DATA_PATH, OUTPUT_DATA_PATH)
    # Energy Areachart
    energy_areachart_fig = energy_area_chart_figure(MAPPINGS_DATA_PATH, INPUT_DATA_PATH, OUTPUT_DATA_PATH)
    # Energy Piechart
    energy_pie_chart_fig = energy_pie_chart_figure(year, MAPPINGS_DATA_PATH, INPUT_DATA_PATH, OUTPUT_DATA_PATH)
    # Emissions Areachart
    emissions_area_chart_fig = emissions_area_chart_figure(MAPPINGS_DATA_PATH, INPUT_DATA_PATH, OUTPUT_DATA_PATH)
    
    return energy_sankey_fig, energy_barchart_fig, energy_pie_chart_fig, energy_areachart_fig, emissions_area_chart_fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8080)