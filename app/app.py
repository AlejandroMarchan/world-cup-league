import requests as r
import logging
import sys
import os
from datetime import datetime, timedelta
import json
import time

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
    '12/03/2022 16:00',
    '12/03/2022 20:00',
    '12/04/2022 16:00',
    '12/04/2022 20:00',
    '12/05/2022 16:00',
    '12/05/2022 20:00',
    '12/06/2022 16:00',
    '12/06/2022 20:00',
    '12/09/2022 16:00',
    '12/09/2022 20:00',
    '12/10/2022 16:00',
    '12/10/2022 20:00',
    '12/13/2022 20:00',
    '12/14/2022 20:00',
    '12/17/2022 16:00',
    '12/18/2022 16:00',
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

DEV_API_TOKEN = ''
DEV_API_EMAIL = ''
DEV_API_PASSWORD = ''
try:
    with open('api_token', 'r') as f:
        DEV_API_TOKEN, DEV_API_EMAIL, DEV_API_PASSWORD = [line.strip() for line in f.readlines()]
except:
    log.info("Couldn't read local cookie")

DEV = DEV_API_TOKEN != ''

# DEV = False

API_TOKEN = os.getenv('API_TOKEN', DEV_API_TOKEN)
API_EMAIL = os.getenv('API_EMAIL', DEV_API_EMAIL)
API_PASSWORD = os.getenv('API_PASSWORD', DEV_API_PASSWORD)

API_CREDS_JSON = {
    'email': API_EMAIL,
    'password': API_PASSWORD,
}

HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-type': 'application/json'
}

# LOAD PREDICTIONS
BASE_DIR = 'app/assets/predictions/'

files = os.listdir(BASE_DIR)

files.sort()

PREDICTIONS = {}

for file in files:

    clean_preds = []

    with open(BASE_DIR + file, 'r') as f:
        preds = f.readlines()

        for pred in preds:
            clean_pred = pred.strip()
            if clean_pred != '':
                clean_preds.append(clean_pred)

    PREDICTIONS[file] = clean_preds

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
    },
    *[
        {
            "name": name.split('.')[0].title(), 
            "id": name,
        }
        for name in files 
    ]
]

TABLE_STYLE_CELL_CONDITIONAL = [
    {'if': {'column_id': 'date'},
        'width': '5vw', 'white-space': 'normal'},
    {'if': {'column_id': 'match'},
        'width': '15vw'},
    {'if': {'column_id': 'result'},
        'width': '5vw'},
    *[
        {'if': {'column_id': name},
        'width': '30vw',}
        for name in files
    ]
]

CLASSIFICATION_COLUMNS = [
    {
        "name": 'Pos.', 
        "id": 'position'
    },
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
    {'if': {'column_id': 'position'},
        'width': '1%'},
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
                'margin-top': '15px',
            }
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Checklist(
                            options=[
                                {"label": "Mostrar fase de Grupos", "value": 1}
                            ],
                            value=[],
                            id="groups-input",
                            switch=True
                        ),
                    ],
                    width="auto"
                ),
            ],
            justify="center",
            align="center",
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
                                    page_size=200,
                                    page_action='native',
                                    sort_action='native',
                                    filter_action='native',
                                    filter_options={'case':'insensitive'},
                                    fixed_rows={'headers': True, 'data': 0},
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
                                        'whiteSpace': 'nowrap',
                                        'height': 'auto',
                                        'padding': '10px',
                                        'text-align': 'center',
                                        'overflow-x': 'auto',
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
                                    page_size=200,
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
                                        'whiteSpace': 'nowrap',
                                        'height': 'auto',
                                        'padding': '10px',
                                        'text-align': 'center',
                                        'overflow-x': 'auto',
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
                'margin-top': '7px',
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
    Input('groups-input', 'value'),
    Output('matchs-table', 'data'),
    Output('classification-table', 'data'),
    Output('matchs-table', 'style_data_conditional'),
)
def load_matches(x, show_groups):
    global HEADERS
    global API_TOKEN

    matches = []
    tic = time.perf_counter()

    if DEV:
        with open('app/assets/matches.json', 'r') as f:
            matches = json.load(f)
    else:
        print('Calling the API')
        response = r.get('http://api.cup2022.ir/api/v1/match', headers=HEADERS)
        try:

            print(f'Response status code: {response.status_code}')

            if response.status_code == 401:
                print('Unauthorized, getting new API token')
                api_res = r.post('http://api.cup2022.ir/api/v1/user/login', json=API_CREDS_JSON)
                API_TOKEN = api_res.json()['data']['token']
                os.environ["API_TOKEN"] = API_TOKEN
                HEADERS = {
                    'Authorization': f'Bearer {API_TOKEN}',
                    'Content-type': 'application/json'
                }
                print('Retrying API call')
                response = r.get('http://api.cup2022.ir/api/v1/match', headers=HEADERS)
                print(f'New response status code: {response.status_code}')


            print('Saving the results.')
            matches = response.json()['data']
            with open('app/assets/matches.json', 'w') as f:
                json.dump(matches, f)
        except:
            print('API call failed, stored matches fallback')
            with open('app/assets/matches.json', 'r') as f:
                matches = json.load(f)
    
    tac = time.perf_counter()
    
    print(f'API call ended in {tac - tic} seconds.')

    tic = time.perf_counter()

    # print(matches)
    matches.sort(key=lambda x: datetime.strptime(x['local_date'], '%m/%d/%Y %H:%M'))

    matches += [
        # {
        #     'home_team_en': 'Paises Bajos',
        #     'away_team_en': 'Estados unidos',
        #     'home_flag': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Flag_of_the_Netherlands.svg/125px-Flag_of_the_Netherlands.svg.png',
        #     'away_flag': 'https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/125px-Flag_of_the_United_States.svg.png',
        #     'home_score': 0,
        #     'away_score': 0,
        #     'type': 'sixteen',
        #     'time_elapsed': 'notstarted',
        #     'local_date': '12/03/2022 18:00',
        # },
    ]

    prev_type = 'group'
    
    match_rows = []
    added_matches = []

    for match in matches:
        home_team = TEAMS_EN_ES.get(match['home_team_en'], match['home_team_en'])
        away_team = TEAMS_EN_ES.get(match['away_team_en'], match['away_team_en'])
        home_flag = match['home_flag']
        away_flag = match['away_flag']
        home_score = match['home_score']
        away_score = match['away_score']
        match_tag = f"{home_team}-{away_team}"
        date = datetime.strptime(match['local_date'], '%m/%d/%Y %H:%M') - timedelta(hours=2)

        if  match_tag == 'Irán-Gales' \
            or match_tag == 'Serbia-Camerún' \
            or match_tag == 'Inglaterra-Gales' \
            or match_tag == 'Dinamarca-Australia' \
            or match_tag == 'Brasil-Camerún' \
            or match['type'] != 'group':
            home_team, away_team = away_team, home_team
            home_flag, away_flag = away_flag, home_flag
            home_score, away_score = away_score, home_score
            match_tag = f"{home_team}-{away_team}"
        
        if match_tag == 'Paises Bajos-Catar':
            home_score = 2
            away_score = 0
        elif match_tag == 'Túnez-Francia':
            home_score = 1
            away_score = 0
        elif match_tag == 'Canadá-Marruecos':
            home_score = 1
            away_score = 2
        elif match_tag == 'Japón-España':
            home_score = 2
            away_score = 1
        elif match_tag == 'Costa Rica-Alemania':
            home_score = 2
            away_score = 4
        elif match_tag == 'Brasil-Portugal':
            home_team = 'Portugal'
            away_team = 'Suiza'
            home_flag = away_flag
            away_flag = 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Flag_of_Switzerland.svg/100px-Flag_of_Switzerland.svg.png'
            match_tag = 'Portugal-Suiza'

        row = {
            'date': date.strftime('%b %d, %Y, %H:%M'),
            'match': f"![home_flag]({home_flag}) **{home_team}** vs **{away_team}** ![away_flag]({away_flag})",
            'match_key': match_tag,
            'home_team': home_team,
            'away_team': away_team,
            'tag': match_tag if match['type'] == 'group' else date.strftime('%m/%d/%Y %H:%M'),
            'result': 'Not started' if match['time_elapsed'] == 'notstarted' else f'{home_score} - {away_score}',
            'type': match['type']
        }

        if match['type'] == 'R16' and prev_type == 'group':
            match_rows.append(
                {
                    'date': '-',
                    'match': f"**OCTAVOS**",
                    'match_key': '',
                    'home_team': '',
                    'away_team': '',
                    'tag': '',
                    'result': 'Not started',
                    'type': ''
                }
            )
        if match['type'] == 'QR' and prev_type == 'R16':
            match_rows.append(
                {
                    'date': '-',
                    'match': f"**CUARTOS**",
                    'match_key': '',
                    'home_team': '',
                    'away_team': '',
                    'tag': '',
                    'result': 'Not started',
                    'type': ''
                }
            )
        if match['type'] == 'semi' and prev_type == 'QR':
            print(row)
            match_rows.append(
                {
                    'date': '-',
                    'match': f"**SEMIS**",
                    'match_key': '',
                    'home_team': '',
                    'away_team': '',
                    'tag': '',
                    'result': 'Not started',
                    'type': ''
                }
            )
        if match['type'] == 'FIN' and prev_type == 'semi':
            match_rows.append(
                {
                    'date': '-',
                    'match': f"**FINAL**",
                    'match_key': '',
                    'home_team': '',
                    'away_team': '',
                    'tag': '',
                    'result': 'Not started',
                    'type': ''
                }
            )

        # print(row['match'])
        print(prev_type)
        print(match['type'])

        prev_type = match['type']

        if match_tag not in added_matches and home_team != '--' and away_team != '--':
            match_rows.append(row)
            added_matches.append(match_tag)


    styles = [
        {
            "if": {"state": "selected"},
            "backgroundColor": "none",
            "border": "1px solid rgb(211, 211, 211)",
        }
    ]

    pred_rows = []

    for file, clean_preds in PREDICTIONS.items():
        pred_row = {
            'nombre': file.split('.')[0].title(),
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
        
        groups_preds =  clean_preds[:48] + \
                        clean_preds[96:104] + \
                        clean_preds[112:116] + \
                        clean_preds[120:122] + \
                        clean_preds[126:128]

        equipos_octavos = clean_preds[80:96]
        equipos_cuartos = clean_preds[104:112]
        equipos_semis = clean_preds[116:120]
        equipos_final = clean_preds[122:126]
        equipo_campeon = clean_preds[-1]

        for match in match_rows:
            try:
                match_idx = MATCH_TAGS.index(match['tag'])

                pred_result = [int(goals) for goals in groups_preds[match_idx].split('|')[1].split('-')]
                match[file] = f'{pred_result[0]} - {pred_result[1]}'

                if match['type'] == 'R16':
                    if match['home_team'] in equipos_octavos:
                        pred_row['octavos'] += 1
                    if match['away_team'] in equipos_octavos:
                        pred_row['octavos'] += 1

                if match['type'] == 'QR':
                    if match['home_team'] in equipos_cuartos:
                        pred_row['cuartos'] += 1
                    if match['away_team'] in equipos_cuartos:
                        pred_row['cuartos'] += 1

                if match['type'] == 'semi':
                    if match['home_team'] in equipos_semis:
                        pred_row['semis'] += 1
                    if match['away_team'] in equipos_semis:
                        pred_row['semis'] += 1

                if match['type'] == 'FIN':
                    if match['home_team'] in equipos_final:
                        pred_row['final'] += 1
                    if match['away_team'] in equipos_final:
                        pred_row['final'] += 1

                # Check if the teams are right
                if match['type'] != 'group' and match['match_key'] != groups_preds[match_idx].split('·')[0]:
                    match[file] = '-'
                elif match['result'] != 'Not started':

                    real_result = [int(goals) for goals in match['result'].split('-')]
                    # print(match['tag'])
                    # print('real_result', real_result)
                    # print('pred_result', pred_result)

                    real_res_symbol = get_res_symbol(real_result)
                    pred_res_symbol = get_res_symbol(pred_result)
                    
                    # Check exact result
                    if real_result[0] == pred_result[0] and real_result[1] == pred_result[1]:
                        # print('res_exacto')
                        pred_row['res_exacto'] += 1
                        styles.append({
                            'if': {
                                'filter_query': '{match} = "' + match['match'] + '"' + ' && {date} = "' + match['date'] + '"', 
                                'column_id': file
                            },
                            'backgroundColor': '#92ff9273',
                        })
                    # Check match result
                    elif real_res_symbol == pred_res_symbol:
                        # print('res_partido')
                        pred_row['res_partido'] += 1
                        styles.append({
                            'if': {
                                'filter_query': '{match} = "' + match['match'] + '"' + ' && {date} = "' + match['date'] + '"', 
                                'column_id': file
                            },
                            'backgroundColor': '#ffff0080',
                        })
                    else:
                        styles.append({
                            'if': {
                                'filter_query': '{match} = "' + match['match'] + '"' + ' && {date} = "' + match['date'] + '"', 
                                'column_id': file
                            },
                            'backgroundColor': '#ff3e3e59',
                        })
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

    pred_rows.sort(key=lambda x: x['total'], reverse=True)

    for i, row in enumerate(pred_rows):
        row['position'] = i + 1
    # print(pred_rows)


    if len(show_groups) == 0:
        match_rows = [row for row in match_rows if row['type'] != 'group']

    tac = time.perf_counter()
    
    print(f'Total data postprocessing took {tac - tic} seconds.')


    return match_rows, pred_rows, styles


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8080, use_reloader=False)
