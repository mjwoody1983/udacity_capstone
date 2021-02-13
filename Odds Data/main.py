import sys
import json
import requests
import argparse
import time
from datetime import datetime
import psycopg2
import pandas as pd


# My API key
API_KEY = '1992c2f27140469ac11c01ef90048c56'

SPORT = []  # populate the league into this variable

REGION = 'uk'  # Need to understand whether this needs to be expanded to capture more data

MARKET = 'h2h'  # spreads | totals are the additional markets that is available, to start only interested in h2h

prefix = 'Soccer'  # Interested initially in soccer only

sports_response = requests.get('https://api.the-odds-api.com/v3/sports', params={
    'api_key': API_KEY
})

sports_json = json.loads(sports_response.text)

print('List of in season sports:', sports_json['data'])

sport = sports_json['data']
outcome = list(filter(lambda league: league['group'].startswith(prefix), sport))
len(outcome)

leagues = [li['key'] for li in outcome]
leagues

odds_list = []
len_leagues = len(leagues)

for x in range(0, len_leagues):
    odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
        'api_key': API_KEY,
        'sport': leagues[x],
        'region': REGION,
        'mkt': MARKET,
    })

    odds_json = json.loads(odds_response.text)
    odds_list.append(odds_json)

odds_len = len(odds_list)
bookmakers = []

for x in range(0, odds_len):
    matches = odds_list[x]['data']
    fixtures = len(matches)

    for x in range(0, fixtures):
        bookmaker = matches[x]
        sites_count = bookmaker['sites_count']

        if sites_count < 2:
            continue

        for x in range(0, sites_count):
            bookmakers.append([
                bookmaker['sport_nice'],
                bookmaker['teams'][0],
                bookmaker['teams'][1],
                bookmaker['commence_time'],
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(bookmaker['commence_time'])),
                bookmaker['home_team'],
                bookmaker['sites'][x]['site_nice'],
                bookmaker['sites'][x]['odds']['h2h'][0],  # result_1
                bookmaker['sites'][x]['odds']['h2h'][1],  # result_2
                bookmaker['sites'][x]['odds']['h2h'][2],  # result_3
                1 / bookmaker['sites'][x]['odds']['h2h'][0],  # result_1_trimmed_or
                1 / bookmaker['sites'][x]['odds']['h2h'][1],  # result_2_trimmed_or
                1 / bookmaker['sites'][x]['odds']['h2h'][2],  # result_3_trimmed_or
                ((1 / bookmaker['sites'][x]['odds']['h2h'][0]) +
                 (1 / bookmaker['sites'][x]['odds']['h2h'][1]) +
                 (1 / bookmaker['sites'][x]['odds']['h2h'][2])  # bookmaker margin. Amount over 1 is their profit
                 )
            ])

df = pd.DataFrame(bookmakers,
                  columns=['league', 'team_0', 'team_1', 'kick_off_epoch', 'kick_off_timestamp', 'home_team',
                           'bookmaker', 'odds_0', 'odds_1', 'odds_2', 'odds_0_or', 'odds_1_or', 'odds_2_or',
                           'bookmaker_margin'])

df['stripped_0'] = df['odds_0_or'] / df['bookmaker_margin']
df['stripped_1'] = df['odds_1_or'] / df['bookmaker_margin']
df['stripped_2'] = df['odds_2_or'] / df['bookmaker_margin']
df['target_0'] = 1 / (df['stripped_0'] / 1)
df['target_1'] = 1 / (df['stripped_1'] / 1)
df['target_2'] = 1 / (df['stripped_2'] / 1)
print(df)