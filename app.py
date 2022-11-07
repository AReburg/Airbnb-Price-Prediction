from dash import Dash, dcc, html, Input, Output
import pandas as pd
from assets import charts
from assets import data_wrangling
from assets import interaction
import xgboost as xgb

df = data_wrangling.import_data()
model = data_wrangling.get_model()

restaurant = data_wrangling.import_csv_to_gpd('restaurant')
cafe = data_wrangling.import_csv_to_gpd('cafe')
attraction = data_wrangling.import_csv_to_gpd('attraction')
station = data_wrangling.import_csv_to_gpd('attraction')
bar = data_wrangling.import_csv_to_gpd('bar')
biergarten = data_wrangling.import_csv_to_gpd('biergarten')
fast_food = data_wrangling.import_csv_to_gpd('fast_food')
pub = data_wrangling.import_csv_to_gpd('pub')
nightclub = data_wrangling.import_csv_to_gpd('nightclub')
theatre = data_wrangling.import_csv_to_gpd('theatre')
university = data_wrangling.import_csv_to_gpd('university')
attraction = data_wrangling.import_csv_to_gpd('attraction')


# set-up webpage layout to display visuals and receives user input text for model
# render web page with plotly graphs
app = Dash(__name__)
server = app.server

app.layout = html.Div([
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


@app.callback(
    [Output('result-histogram', 'figure'), Output('tokenized_text', 'children')],
    Input("input_text", "value"))
def update_categories(input_text):
    """ use model to predict benchmark price for input address"""
    preds = ''
    if input_text == '' or input_text is None:
        pass
    # Universitätsring 2, 1010 Wien
    # Fleischmarkt 20/Wolfengasse 3
    else:
        dfi = data_wrangling.parse_input(input_text)
        dfi[['longitude', 'latitude']] = dfi.apply(lambda x: data_wrangling.get_lat_long(x['geometry']), axis=1)

        parameters = [restaurant, cafe, bar, station, biergarten, fast_food, pub, nightclub, theatre, university,
                      attraction]
        names = ['restaurant', 'cafe', 'bar', 'station', 'biergarten', 'fast_food', 'pub', 'nightclub', 'theatre',
                 'university', 'attraction']
        print(dfi.head())
        X_pred = data_wrangling.main(dfi, parameters, names)
        print(X_pred.head())
        preds = model.predict(X_pred)
        print(preds)

    return [str(preds), '']


if __name__ == "__main__":
    app.run_server(debug=False)

