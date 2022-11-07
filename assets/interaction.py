# -*- coding: utf-8 -*-
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path
import geojson
from dash import Dash, dcc, html, Input, Output

# Define color sets of paintings
night_colors = ['rgb(56, 75, 126)', 'rgb(18, 36, 37)', 'rgb(34, 53, 101)']
cwd = Path().resolve()

from assets import charts
from assets import data_wrangling
import xgboost as xgb




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