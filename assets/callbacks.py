from pathlib import Path
#from app import data_wrangling
import xgboost as xgb
from dash.dependencies import Output, Input
cwd = Path().resolve()
from assets.data_wrangling import GeoData
data = GeoData()

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
            dfi = data.parse_input(input_text)
            dfi[['longitude', 'latitude']] = dfi.apply(lambda x: data.get_lat_long(x['geometry']), axis=1)

            print(dfi.head())
            X_pred = data.main(dfi, parameters, names)
            print(X_pred.head())
            preds = round(float(model.predict(X_pred)),2)
            preds = f'{preds} $'

        return [str(preds), preds]