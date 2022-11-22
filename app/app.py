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

MATCH_TAGS = [
    'Senegal-Paises Bajos',
    'Catar-Ecuador',
    'Inglaterra-Irán',
    'Estados unidos-Gales',
    'Argentina-Arabia Saudita',
    'México-Polonia',
    'Dinamarca-Túnez',
    'Francia-Australia',
    'Alemania-Japón',
    'España-Costa Rica',
    'Marruecos-Croacia',
    'Bélgica-Canadá',
    'Suiza-Camerún',
    'Brasil-Serbia',
    'Uruguay-Corea del Sur',
    'Portugal-Ghana',
    'Catar-Senegal',
    'Paises Bajos-Ecuador',
    'Gales-Irán',
    'Inglaterra-Estados unidos',
    'Polonia-Arabia Saudita',
    'Argentina-México',
    'Túnez-Australia',
    'Francia-Dinamarca',
    'Japón-Costa Rica',
    'España-Alemania',
    'Bélgica-Marruecos',
    'Croacia-Canadá',
    'Camerún-Serbia',
    'Brasil-Suiza',
    'Corea del Sur-Ghana',
    'Portugal-Uruguay',
    'Ecuador-Senegal',
    'Paises Bajos-Catar',
    'Gales-Inglaterra',
    'Irán-Estados unidos',
    'Polonia-Argentina',
    'Arabia Saudita-México',
    'Australia-Dinamarca',
    'Túnez-Francia',
    'Japón-España',
    'Costa Rica-Alemania',
    'Croacia-Bélgica',
    'Canadá-Marruecos',
    'Serbia-Suiza',
    'Camerún-Brasil',
    'Ghana-Uruguay',
    'Corea del Sur-Portugal',
]

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
    'Nederlands': 'Paises Bajos',
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

DEV_API_TOKEN = ''
try:
    DEV_API_TOKEN = open('api_token', 'r').read()
except:
    log.info("Couldn't read local cookie")

API_TOKEN = os.getenv('API_TOKEN', DEV_API_TOKEN)

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

CLASSIFICATION_COLUMNS = [
    {
        "name": 'Nombre participante', 
        "id": 'nombre'
    },
    {
        "name": 'Total ptos', 
        "id": 'total',
    },
    {
        "name": 'Res. exacto (5 ptos)', 
        "id": 'res_exacto'
    },
    {
        "name": 'Res. partido (2 ptos)', 
        "id": 'res_partido',
    },
    {
        "name": 'Eq. octavos (6 ptos)', 
        "id": 'octavos',
    },
    {
        "name": 'Eq. cuartos (12 ptos)', 
        "id": 'cuartos',
    },
    {
        "name": 'Eq. semis (24 ptos)', 
        "id": 'semis',
    },
    {
        "name": 'Eq. final (48 ptos)', 
        "id": 'final',
    },
    {
        "name": 'Eq. campeón (50 ptos)', 
        "id": 'campeon',
    }
]

CLASSIFICATION_TABLE_STYLE_CELL_CONDITIONAL = [
    {'if': {'column_id': 'nombre'},
        'width': '20%'},
    {'if': {'column_id': 'total'},
        'width': '10%'},
    {'if': {'column_id': 'res_exacto'},
        'width': '10%'},
    {'if': {'column_id': 'res_partido'},
        'width': '10%'},
    {'if': {'column_id': 'octavos'},
        'width': '10%'},
    {'if': {'column_id': 'cuartos'},
        'width': '10%'},
    {'if': {'column_id': 'semis'},
        'width': '10%'},
    {'if': {'column_id': 'final'},
        'width': '10%'},
    {'if': {'column_id': 'campeon'},
        'width': '10%'},
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
                    ],
                    width='auto',
                    style={
                        'margin-bottom': '50px',
                    }
                ),
                dbc.Col(
                    [
                        dcc.Loading(
                            id="loading-class-table",
                            type="default",
                            children=[
                                dash_table.DataTable(
                                    id='classification-table',
                                    columns=CLASSIFICATION_COLUMNS,
                                    page_size=20,
                                    page_action='native',
                                    sort_action='native',
                                    filter_action='native',
                                    filter_options={'case':'insensitive'},
                                    style_as_list_view=True,
                                    style_cell_conditional=CLASSIFICATION_TABLE_STYLE_CELL_CONDITIONAL,
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
                    ],
                    width='auto',
                    style={
                        'margin-bottom': '50px',
                    }
                ),
            ],
            justify="center",
            align="center",
            style={
                'margin-top': '30px',
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
        'width': '100vw',
        'margin': 'auto',
        'height': '100vh',
        'display': 'flex',
        'flex-direction': 'column' 
    }
)

def get_res_symbol(result):
    res_symbol = '1'
    if result[0] < result[1]:
        res_symbol = '2'
    elif result[0] == result[1]:
        res_symbol = 'X'

    return res_symbol

@app.callback(
    Input('placeholder', 'title'),
    Output('matchs-table', 'data'),
    Output('classification-table', 'data'),
)
def load_matches(x):
    matches = []
    try:
        response = r.get('http://api.cup2022.ir/api/v1/match', headers=HEADERS)

        matches = response.json()['data']
    except:
        log.info('API call failed')

    # import json
    # with open('tests/matches.json', 'r') as f:
    #     matches = json.load(f)

    # print(matches)
    matches.sort(key=lambda x: x['local_date'])
    
    match_rows = []

    for match in matches:
        home_team = TEAMS_EN_ES.get(match['home_team_en'], match['home_team_en'])
        away_team = TEAMS_EN_ES.get(match['away_team_en'], match['away_team_en'])
        home_flag = match['home_flag']
        away_flag = match['away_flag']
        date = datetime.strptime(match['local_date'], '%m/%d/%Y %H:%M') - timedelta(hours=2)

        row = {
            'date': date.strftime('%b %d, %Y, %H:%M:%S'),
            'match': f"![home_flag]({home_flag}) **{home_team}** vs **{away_team}** ![away_flag]({away_flag})",
            'tag': f"{home_team}-{away_team}",
            'result': 'Not started' if match['time_elapsed'] == 'notstarted' else f'{match["home_score"]} - {match["away_score"]}',
        }

        match_rows.append(row)

    pred_rows = []

    base_dir = 'app/assets/predictions/'

    files = os.listdir(base_dir)

    for file in files:
        pred_row = {
            'nombre': file.split('.')[0].capitalize(),
            'total': 0,
            'res_exacto': 0,
            'res_partido': 0,
            'octavos': 0,
            'cuartos': 0,
            'semis': 0,
            'final': 0,
            'campeon': 0,
        }
        # print(f'[bold]{pred_row["nombre"]}')

        clean_preds = []

        with open(base_dir + file, 'r') as f:
            preds = f.readlines()

            for pred in preds:
                clean_pred = pred.strip()
                if clean_pred != '':
                    clean_preds.append(clean_pred)
        
        groups_preds = clean_preds[:48]

        for match in match_rows:
            try:
                if match['result'] == 'Not started':
                    break

                match_idx = MATCH_TAGS.index(match['tag'])

                real_result = [int(goals) for goals in match['result'].split('-')]
                pred_result = [int(goals) for goals in groups_preds[match_idx].split('|')[1].split('-')]
                # print(match['tag'])
                # print('real_result', real_result)
                # print('pred_result', pred_result)

                # Check exact result
                if real_result[0] == pred_result[0] and real_result[1] == pred_result[1]:
                    # print('res_exacto')
                    pred_row['res_exacto'] += 1

                real_res_symbol = get_res_symbol(real_result)
                pred_res_symbol = get_res_symbol(pred_result)
                
                # Check match result
                if real_res_symbol == pred_res_symbol:
                    # print('res_partido')
                    pred_row['res_partido'] += 1

                # print()

            except:
                log.info(f'Error parsing {pred_row["nombre"]} predictions')

        # Compute points
        pred_row['total'] = pred_row['res_exacto'] * 5 + \
                            pred_row['res_partido'] * 2 + \
                            pred_row['octavos'] * 6 + \
                            pred_row['cuartos'] * 12 + \
                            pred_row['semis'] * 24 + \
                            pred_row['final'] * 48 + \
                            pred_row['campeon'] * 50

        pred_rows.append(pred_row)

    pred_rows.sort(key=lambda x: x['total'])
    # print(pred_rows)

    return match_rows, pred_rows


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8080, use_reloader=False)
