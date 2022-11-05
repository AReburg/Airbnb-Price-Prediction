from dash import Dash, dcc, html, Input, Output
import pandas as pd
from assets import charts
from assets import data_wrangling

df = data_wrangling.import_data()


# set-up webpage layout to display cool visuals and receives user input text for model
# render web page with plotly graphs
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    # left half of the web page
    html.Div([
        html.Div([html.Img(src=app.get_asset_url('logo.png'), height='25 px', width='auto')],
                className = 'col-2', style={'align-items': 'center', 'padding-top' : '1%', 'height' : 'auto'}),
        html.H2('Disaster Response Project'),
        html.P("Analyzing message data for  disaster response."),
        html.Br(),
        html.P("""hiere kommt geiler Text herein"""),
        html.Div([f"The data set consists of {df.shape[0]} samples:"], className='text-padding'),
        #html.Div([dcc.Graph(figure=charts.get_pie_chart(df), config={'displayModeBar': False})], style={'width': '250px', 'align-items': 'center'}),
        html.Div([dcc.Graph(figure=charts.heatmap_airbnb(df), config={'displayModeBar': False})]),
        ], className='four columns div-user-controls'),

    # right half of the web page
    html.Div([
        html.Div(
            [
            html.Br(),
            html.Br(),
            html.Br(),
                html.H4("Enter a message and hit enter"),

                html.Div(
                    children=[dcc.Input(id="input_text", type="text", placeholder="", debounce=True,
                                        style={'border-radius': '8px', #'border': '4px solid red'
                                            'background-color': '#31302f', 'color': 'white',
                                            'width': '100%',
                                                            'padding':'5px'})],  # fill out your Input however you need
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
    """ use model to predict classification for input text query """
    if input_text == '' or input_text is None:
        df_res = pd.DataFrame(data={'cate': [i.replace("_", " ").title() for i in df.columns[2:]],
                                    'val': [0 for _ in df.columns[2:]]})
        tokenized_text = ""

    else:
        classification_labels = model.predict([input_text])[0]
        classification_results = dict(zip(df.columns[2:], classification_labels))
        df_res = pd.DataFrame(data={'cate': [i.replace("_"," ").title() for i in list(classification_results.keys())],
                                 'val': classification_results.values()})
        tokenized_text = ", ".join(str(x) for x in tokenize(input_text))

    return [charts.get_main_chart(df_res), tokenized_text]


if __name__ == "__main__":
    app.run_server(debug=False)

