from dash import dcc, html
import pandas as pd
from assets import charts
import logging

def layout(df):

    layout = html.Div([
        # left half of the web page
        html.Div([
            #html.Div([html.Img(src=app.get_asset_url('logo.png'), height='25 px', width='auto')],
            #        className = 'col-2', style={'align-items': 'center', 'padding-top' : '1%', 'height' : 'auto'}),
            html.H2('Airbnb Benchmark Price Prediction'),
            # html.H3('How to price an airbnb propery based on OpenStreetMap features?'),
            # html.Br(),
            html.P("""This project aims at predicting Airbnb host charging prices of a potential new listing across Vienna.
            There is public information available about roughly 12,000 Airbnb listings and their hosts.
            
            A machine learning pipline has been established, where OSM features are used for price modelling. These features include
            the location of amenities such as shops, bars, restaurants, tourist destinations etc.
            """),
            # html.Div([f"The data set consists of {df.shape[0]} samples:"], className='text-padding'),
            html.Div([dcc.Graph(figure=charts.heatmap_airbnb(df), config={'displayModeBar': False})]),
            ], className='four columns div-user-controls'),

        # right half of the web page
        html.Div([
            html.Div(
                [
                html.Br(),
                html.Br(),
                html.Br(),
                    html.H4("Type in an address in Vienna:"),
                    html.Div(
                        children=[dcc.Input(id="input_text", type="text", placeholder="", debounce=True,
                                            style={'border-radius': '8px', #'border': '4px solid red'
                                                'background-color': '#31302f', 'color': 'white',
                                                'width': '100%', 'padding':'5px'})],  # fill out your Input however you need
                        style=dict(display='flex', justifyContent='center')
                    ),
                    html.Br(),
                    html.Div(id="tokenized_text"),
                ]
            ),
            html.Br(),
            html.Br(),
            html.Br(),
            html.H2(f"Categorization based on the {len(df.columns[2:])} pre-defined topics"),
            html.Br(),
            html.Div([dcc.Graph(id='result-histogram', figure={}, config={'displayModeBar': False},
                                style={'height': '900px', 'width': '1200px'})], className='dash-graph')
        ], className='eight columns div-for-charts bg-grey')
    ])
    return layout

