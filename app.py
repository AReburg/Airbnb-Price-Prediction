# from dash import Dash, dcc, html, Input, Output
from assets.data_wrangling import GeoData
import dash
from assets.layout import layout
from assets.callbacks import register_callbacks


import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler


logger = logging.getLogger(__name__)

logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey=d989e5c0-698b-4b3e-a645-18ac1f273b59')
)
data = GeoData()
df = data.import_data()
model = data.get_model()

restaurant = data.import_csv_to_gpd('restaurant')
cafe = data.import_csv_to_gpd('cafe')
attraction = data.import_csv_to_gpd('attraction')
station = data.import_csv_to_gpd('attraction')
bar = data.import_csv_to_gpd('bar')
biergarten = data.import_csv_to_gpd('biergarten')
fast_food = data.import_csv_to_gpd('fast_food')
pub = data.import_csv_to_gpd('pub')
nightclub = data.import_csv_to_gpd('nightclub')
theatre = data.import_csv_to_gpd('theatre')
university = data.import_csv_to_gpd('university')
attraction = data.import_csv_to_gpd('attraction')
parameters = [restaurant, cafe, bar, station, biergarten, fast_food, pub, nightclub, theatre, university,
              attraction]
names = ['restaurant', 'cafe', 'bar', 'station', 'biergarten', 'fast_food', 'pub', 'nightclub', 'theatre',
         'university', 'attraction']


dash_app = dash.Dash(__name__)
dash_app.title = 'Dashboard'
app = dash_app.server


dash_app.layout = layout(df)
register_callbacks(dash_app, df, model, parameters, names)


if __name__ == "__main__":
    dash_app.run_server(debug=True)

