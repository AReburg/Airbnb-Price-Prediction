from pathlib import Path
#from app import data_wrangling
import xgboost as xgb
from dash.dependencies import Output, Input
cwd = Path().resolve()
from assets.data_wrangling import GeoData
data = GeoData()
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey=d989e5c0-698b-4b3e-a645-18ac1f273b59')
)

def register_callbacks(app, df, model, parameters, names):
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
            logger.exception(f'input text: {input_text}')
            try:
                dfi = data.parse_input(input_text)
                dfi[['longitude', 'latitude']] = dfi.apply(lambda x: data.get_lat_long(x['geometry']), axis=1)
            except Exception as e:
                logger.exception(f"Errroin in pared_input: {e}")
            logger.warning(f"{dfi['longitude'].item()}")
            # print(dfi.head())
            try:
                X_pred = data.main(dfi, parameters, names)
            except Exception as e:
                logger.exception(f'X_pred exception: {e}')
            # print(X_pred.head())
            preds = round(float(model.predict(X_pred)),2)
            # preds = f'{preds} $'

        return [str(preds), preds]