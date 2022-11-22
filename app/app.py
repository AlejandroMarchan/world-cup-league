import requests as r
import logging
import sys
import os
from datetime import datetime, timedelta

# Init logging
logging.basicConfig(
    format='[%(asctime)s] [%(name)s:%(lineno)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %z',
    stream=sys.stdout,
    level=10
)

log = logging.getLogger("PIL")
log.setLevel(logging.INFO)

log = logging.getLogger("urllib3.connectionpool")
log.setLevel(logging.INFO)

log = logging.getLogger("app")
log.setLevel(logging.INFO)

import requests as r
from rich import print

TEAMS_ES_EN = {
    'Catar': 'Qatar',
    'Ecuador': 'Ecuador',
    'Senegal': 'Senegal',
    'Paises Bajos': 'Netherlands',
    'Inglaterra': 'England',
    'Irán': 'Iran',
    'Estados unidos': 'United States',
    'Gales': 'Wales',
    'Argentina': 'Argentina',
    'Arabia Saudita': 'Saudi Arabia',
    'México': 'Mexico',
    'Polonia': 'Poland',
    'Francia': 'France',
    'Dinamarca': 'Denmark',
    'Túnez': 'Tunisia',
    'Australia': 'Australia',
    'España': 'Spain',
    'Costa Rica': 'Costa Rica',
    'Alemania': 'Germany',
    'Japón': 'Japan',
    'Bélgica': 'Belgium',
    'Canadá': 'Canada',
    'Marruecos': 'Morocco',
    'Croacia': 'Croatia',
    'Brasil': 'Brazil',
    'Serbia': 'Serbia',
    'Suiza': 'Switzerland',
    'Camerún': 'Cameroon',
    'Portugal': 'Portugal',
    'Ghana': 'Ghana',
    'Uruguay': 'Uruguay',
    'Corea del Sur': 'South Korea',
}

TEAMS_EN_ES = {
    'Qatar': 'Catar',
    'Ecuador': 'Ecuador',
    'Senegal': 'Senegal',
    'Netherlands': 'Paises Bajos',
    'England': 'Inglaterra',
    'Iran': 'Irán',
    'United States': 'Estados unidos',
    'Wales': 'Gales',
    'Argentina': 'Argentina',
    'Saudi Arabia': 'Arabia Saudita',
    'Mexico': 'México',
    'Poland': 'Polonia',
    'France': 'Francia',
    'Denmark': 'Dinamarca',
    'Tunisia': 'Túnez',
    'Australia': 'Australia',
    'Spain': 'España',
    'Costa Rica': 'Costa Rica',
    'Germany': 'Alemania',
    'Japan': 'Japón',
    'Belgium': 'Bélgica',
    'Canada': 'Canadá',
    'Morocco': 'Marruecos',
    'Croatia': 'Croacia',
    'Brazil': 'Brasil',
    'Serbia': 'Serbia',
    'Switzerland': 'Suiza',
    'Cameroon': 'Camerún',
    'Portugal': 'Portugal',
    'Ghana': 'Ghana',
    'Uruguay': 'Uruguay',
    'South Korea': 'Corea del Sur',
}


API_TOKEN = os.getenv('API_TOKEN', open('api_token', 'r').read())

HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-type': 'application/json'
}

COLUMNS = [
    {
        "name": 'Date', 
        "id": 'date'
    },
    {
        "name": 'Home vs Away', 
        "id": 'match',
        "presentation": "markdown"
    },
    {
        "name": 'Result', 
        "id": 'result',
    }
]

TABLE_STYLE_CELL_CONDITIONAL = [
    {'if': {'column_id': 'date'},
        'width': '35%'},
    {'if': {'column_id': 'match'},
        'width': '50%'},
    {'if': {'column_id': 'result'},
        'width': '15%',},
]

import dash
from dash_extensions.enrich import DashProxy, MultiplexerTransform, LogTransform, NoOutputTransform
from dash_extensions.enrich import Input, Output, State, html, dcc, dash_table
import dash_bootstrap_components as dbc

app = DashProxy(
    __name__, 
    title="World cup league", 
    transforms=[
        MultiplexerTransform(),  # makes it possible to target an output multiple times in callbacks
        NoOutputTransform(),
        LogTransform()  # makes it possible to write log messages to a Dash component
    ],
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)
app.config.suppress_callback_exceptions = True
server = app.server

app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H1(["World cup league"]),
                    width="auto"
                ),
            ],
            justify="center",
            align="center",
            style={
                'margin-top': '30px',
            }
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Loading(
                            id="loading-table",
                            type="default",
                            children=[
                                dash_table.DataTable(
                                    id='matchs-table',
                                    columns=COLUMNS,
                                    page_size=20,
                                    page_action='native',
                                    sort_action='native',
                                    filter_action='native',
                                    filter_options={'case':'insensitive'},
                                    style_as_list_view=True,
                                    style_cell_conditional=TABLE_STYLE_CELL_CONDITIONAL,
                                    style_data_conditional=[
                                        {
                                            "if": {"state": "selected"},
                                            "backgroundColor": "none",
                                            "border": "1px solid rgb(211, 211, 211)",
                                        }
                                    ],
                                    style_data={
                                        'whiteSpace': 'normal',
                                        'height': 'auto',
                                        'text-align': 'center',
                                        'overflow-x': 'auto',
                                        'max-width': '0'
                                    },
                                    style_header={
                                        'font-weight': 'bold',
                                        'text-align': 'center',
                                        "backgroundColor": "#e1e1e142",
                                        'padding': '10px',
                                        'height': '50px'
                                    },
                                    style_cell={
                                        'font-family':'sans-serif'
                                    },
                                    style_filter={
                                        "backgroundColor": "#e1e1e142",
                                        'text-align': 'center',
                                        'height': '30px',
                                        "color": "black"
                                    }
                                ),
                            ]
                        ),
                    ]
                ),
            ],
            justify="center",
            align="center",
            style={
                'margin-top': '30px',
                'margin-bottom': '20px',
            }
        ),
        html.P(
            id='placeholder',
            style={
                'display': 'none'
            }
        )
    ],
    style={
        'width': '90%',
        'margin': 'auto',
        'height': '100vh',
        'display': 'flex',
        'flex-direction': 'column' 
    }
)

@app.callback(
    Input('placeholder', 'title'),
    Output('matchs-table', 'data'),
)
def load_matches(x):
    matches = []
    try:
        response = r.get('http://api.cup2022.ir/api/v1/match', headers=HEADERS)

        matches = response.json()['data']
    except:
        log.info('API call failed')

    print(matches)
    # import json
    # with open('tests/matches.json', 'r') as f:
    #     matches = json.load(f)

    rows = []

    for match in matches:
        home_team = TEAMS_EN_ES.get(match['home_team_en'], match['home_team_en'])
        away_team = TEAMS_EN_ES.get(match['away_team_en'], match['away_team_en'])
        home_flag = match['home_flag']
        away_flag = match['away_flag']
        date = datetime.strptime(match['local_date'], '%m/%d/%Y %H:%M') - timedelta(hours=2)

        row = {
            'date': date.strftime('%b %d, %Y, %H:%M:%S'),
            'match': f"![home_flag]({home_flag}) **{home_team}** vs **{away_team}** ![away_flag]({away_flag})",
            'result': 'Not started' if match['time_elapsed'] == 'notstarted' else f'{match["home_score"]} - {match["away_score"]}',
        }

        rows.append(row)

    return rows


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8080, use_reloader=False)
