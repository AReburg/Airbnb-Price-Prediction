import dash
import logging
import time
from assets.layout import layout
from assets.data_wrangling import GeoData
from assets.callbacks import register_callbacks
from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey=d989e5c0-698b-4b3e-a645-18ac1f273b59'))


dash_app = dash.Dash(__name__)
dash_app.title = 'Airbnb Price Modelling'
app = dash_app.server

"""
from flask_caching import Cache
cache = Cache(app, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})
TIMEOUT = 60
@cache.memoize(timeout=TIMEOUT)
"""

def query_data():

    t0 = time.time()
    data = GeoData()
    df = data.import_data()
    model = data.get_model()
    region = data.get_region()
    districts = data.get_geo_data()


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
    shop = data.import_csv_to_gpd('supermarket')
    parameters = [restaurant, cafe, bar, station, biergarten, fast_food, pub, nightclub, theatre, university,
                  attraction, shop]
    names = ['restaurant', 'cafe', 'bar', 'station', 'biergarten', 'fast_food', 'pub', 'nightclub', 'theatre',
             'university', 'attraction', 'supermarket']
    print("import took: ", time.time()-t0)
    return df, model, region, districts, parameters, names


df, model, region, districts, parameters, names = query_data()
dash_app.config['suppress_callback_exceptions'] = True


dash_app.layout = layout(dash_app, df, districts, parameters, names)
register_callbacks(dash_app, df, model, region, districts, parameters, names)


if __name__ == "__main__":
    dash_app.run_server(debug=True)

