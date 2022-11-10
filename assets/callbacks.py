from pathlib import Path
#from app import data_wrangling
import xgboost as xgb
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
cwd = Path().resolve()
from assets.data_wrangling import GeoData
from assets import charts
from dash import dcc, html
data = GeoData()
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey=d989e5c0-698b-4b3e-a645-18ac1f273b59')
)


def register_callbacks(app, df, model, region, parameters, names):

    @app.callback(Output('tabs-content-example-graph', 'children'),
                 Input('tabs-example-graph', 'value'))
    def render_content(tab):
        if tab == 'tab-1-listings':
            return html.Div([
            dcc.Graph(figure=charts.heatmap_airbnb_prices(df), config={'displayModeBar': False},
             )], className='dash-graph')
        elif tab == 'tab-2-prices':
            return html.Div([
            dcc.Graph(figure=charts.heatmap_airbnb_listings(df), config={'displayModeBar': False},
             )], className='dash-graph')
        else:
            return html.Div([
            dcc.Graph(figure=charts.heatmap_airbnb_prices(df), config={'displayModeBar': False},
             )], className='dash-graph')

    @app.callback(
        [Output('tokenized_text', 'children'), Output('result-histogram', 'figure')],
        Input("input_text", "value"))
    def update_categories(input_text):
        """ use model to predict benchmark price for input address
        e.g. # Universitätsring 2, 1010 Wien
        Fleischmarkt 20, Wien
        important: https://stackoverflow.com/questions/69964486/plotly-dash-how-to-prevent-figure-from-appearing-when-no-dropdown-value-is-sele
        """
        if input_text == '' or input_text is None:
            return [html.P(" "), charts.get_main_chart(None)]

        else:
            logger.exception(f'input text: {input_text}')
            dfi = data.parse_input(input_text)
            try:
                dfi[['longitude', 'latitude']] = dfi.apply(lambda x: data.get_lat_long(x['geometry']), axis=1)
            except:
                return [html.P("Address could not be found."), charts.get_main_chart(None)]
            if not data.check_if_coord_in_poly(region, dfi['longitude'].item(), dfi['latitude'].item()):
                return [html.P("Not a valid address in Vienna, Austria. Try again."), charts.get_main_chart(None)]
            else:
                try:
                    X_pred = data.main(dfi, parameters, names)
                    preds = round(float(model.predict(X_pred)), 2)
                    return [html.P(f"Point({dfi['longitude'].item()}, {dfi['latitude'].item()}) results in a  {preds} $ benchmark price."), charts.get_main_chart(X_pred)]
                except Exception as e:
                    logger.exception(f'X_pred exception: {e}')
                    return [html.P("Error in price prediction."), charts.get_main_chart(None)]

