import sys
import psycopg2
import pandas as pd
import datetime as dt
import json
import requests
import time
import chardet
import numpy as np
from io import StringIO
from urllib.request import urlopen
from decouple import config
from sports_data.database_connection import Database
from sports_data.database_connection import CursorFromConnectionPool
from sports_data.sql_queries import *

Database.initialise()

# Connection parameters
param_dic = {
    "host": config('HOST'),
    "database": config('DATABASE'),
    "user": config('USER'),
    "password": config('PASSWORD')
}

now = dt.datetime.now()

# ***********************************************************************************
#                       VARIABLES SECTION FOR FUNCTION
# ***********************************************************************************
# leagues by season csv file contains all of the leagues that we want to load through.
url_path = 'https://www.football-data.co.uk/mmz4281/'
start_year = 1993
final_year = now.year - 1
files = open('leagues_by_season.csv')
files_to_load = files.read().split(",")
# Extra leagues, single file source - no seasons to loop
url_ext_path = 'https://www.football-data.co.uk/'
files_ext = open('extra_leagues.csv')
files_to_load_ext = files_ext.read().split(",")

filesLoad = ['e0.csv', 'e1.csv', 'e2.csv', 'e3.csv',  'EC.csv', 'b1.csv', 'd2.csv', 'f1.csv', 'f2.csv',
             'n1.csv', 'p1.csv', 'sc0.csv', 'sc1.csv', 'sc2.csv', 'sc3.csv', 'sp2.csv', 't1.csv',
             'd1.csv', 'sp1.csv', 'i1.csv', 'i2.csv', 'g1.csv']

# loop through each year and create season code for every season
seasons = []
for year in range(start_year, final_year):
    season_start = str(year)
    season_end = str(year + 1)
    year_url = season_start[-2:] + season_end[-2:]
    seasons.append(year_url)


def process_history_results():
    arc_results = []
    for files in filesLoad:
        for y in seasons:
            try:
                print(y)
                print(url_path + y + '/' + files)
                fd = urlopen(url_path + y + '/' + files)
                cDet = chardet.detect(urlopen(url_path + y + '/' + files).read())
                e_coding = cDet.get('encoding')
                df = pd.read_csv(fd, encoding=e_coding, error_bad_lines=False)
                df['season'] = y
                print('File loaded')
                arc_results.append(df)
            except Exception as e:
                print('logging_exception and continuing')
                file_missing = url_path + y + '/' + files
                print(file_missing)
                continue
    frame = pd.concat(arc_results, ignore_index=True)
    frame = frame[['season', 'Div', 'Date', 'Time', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HTR', 'HS', 'AS',
                   'B365H', 'B365D', 'B365A', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA', 'PSH', 'PSD', 'PSA', 'WHH', 'WHD', 'WHA', 'VCH', 'VCD', 'VCA',
                   'MaxH', 'MaxD', 'MaxA', 'AvgH', 'AvgD', 'AvgA']]
    frame.head().to_csv('checking_headings.csv')
    return frame


def process_extra_results():
    extra_results = []

    for f in files_to_load_ext:
        try:
            print(f)
            print(url_ext_path + f.replace("'", ""))
            fd = urlopen(url_ext_path + f.replace("'", ""))
            c_det = chardet.detect(urlopen(url_ext_path + f.replace("'", "")).read())
            e_coding = c_det.get('encoding')
            df = pd.read_csv(fd, encoding=e_coding)
            print('Extra File loaded: ' + f)
            extra_results.append(df)
        except Exception as e:
            print('logging_exception and continuing')
            continue
    frame_extra = pd.concat(extra_results)
    return frame_extra


def process_fixture_data():
    try:
        print(url_ext_path + '/fixtures.csv')
        fd_fix = urlopen(url_ext_path + '/fixtures.csv')
        fix_df = pd.read_csv(fd_fix, encoding='Windows-1252')
        fix_df = fix_df[
            ['Div', 'Date', 'Time', 'HomeTeam', 'AwayTeam', 'B365H', 'B365D', 'B365A', 'BWH', 'BWD', 'BWA', 'IWH',
             'IWD',
             'IWA', 'PSH', 'PSD', 'PSA', 'WHH', 'WHD', 'WHA', 'VCH', 'VCD', 'VCA', 'MaxH', 'MaxD', 'MaxA', 'AvgH',
             'AvgD', 'AvgA'
             ]]

        with CursorFromConnectionPool() as cursor:
            check_load = "select * from staging_fixtures where home_team = '{}' and away_team = '{}' and fixture_date = '{}'".format(
                fix_df['HomeTeam'][0], fix_df['AwayTeam'][0], fix_df['Date'][0])
            print(check_load)
            cursor.execute(check_load)
            record_match = cursor.fetchone() is not None
            print(record_match)
            if record_match:
                return print('Records already exists for this fixture')
            else:
                for i, row in fix_df.iterrows():
                    print(i)
                    cursor.execute(fixtures_insert, list(row))
            print('insert completed')

    except Exception as e:
        print('logging_exception and continuing')


def process_current_season():
    current_season = []

    for f in filesLoad:
        try:
            if now.month > 7:
                season_start = str(now.year)
                season_end = str(now.year + 1)
                year_url = season_start[-2:] + season_end[-2:]
            else:
                season_start = str(now.year - 1)
                season_end = str(now.year)
                year_url = season_start[-2:] + season_end[-2:]
            print(f)
            print(url_path + year_url + '/' + f)
            fd = urlopen(url_path + year_url + '/' + f)
            c_det = chardet.detect(urlopen(url_path + year_url + '/' + f).read())
            e_coding = c_det.get('encoding')
            df = pd.read_csv(fd, encoding=e_coding)
            df['season'] = '2021'
            print('Current Season File loaded: ' + f)
            current_season.append(df)
        except Exception as e:
            print('logging_exception and continuing')
            continue
    frame_current_season = pd.concat(current_season)
    frame_current_season = frame_current_season[
        ['season','Div', 'Date', 'Time', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HTR', 'Referee',
         'HS', 'AS', 'HST', 'AST', 'HF',
         'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD',
         'IWA', 'PSH', 'PSD', 'PSA', 'WHH',
         'WHD', 'WHA', 'VCH', 'VCD', 'VCA', 'MaxH', 'MaxD', 'MaxA', 'AvgH', 'AvgD', 'AvgA']]
    print(frame_current_season)

    with CursorFromConnectionPool() as cursor:
        for i, row in frame_current_season.iterrows():
            print(i)
            cursor.execute(current_season_insert, list(row))

    print('insert completed')


def odds_api_data():
    API_KEY = config('api_key')

    SPORT = []  # populate the league into this variable

    REGION = 'uk'  # Start with just the UK region

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
    df['id'] = np.nan
    df['stripped_0'] = df['odds_0_or'] / df['bookmaker_margin']
    df['stripped_1'] = df['odds_1_or'] / df['bookmaker_margin']
    df['stripped_2'] = df['odds_2_or'] / df['bookmaker_margin']
    df['target_0'] = 1 / (df['stripped_0'] / 1)
    df['target_1'] = 1 / (df['stripped_1'] / 1)
    df['target_2'] = 1 / (df['stripped_2'] / 1)
    df = df[['league', 'team_0', 'team_1', 'kick_off_epoch', 'kick_off_timestamp', 'home_team',
           'bookmaker', 'odds_0', 'odds_1', 'odds_2', 'odds_0_or', 'odds_1_or', 'odds_2_or',
           'bookmaker_margin', 'stripped_0', 'stripped_1', 'stripped_2', 'target_0', 'target_1', 'target_2']]
    print(df)
    df.to_csv('odds.csv', index=False)
    return df


def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    print("Connection successful")
    return conn


def copy_from_stringio(conn, df, table):
    """
    Here we are going save the dataframe in memory
    and use copy_from() to copy it to the table
    """
    df['created_date'] = pd.Timestamp(now)
    # save dataframe to an in memory buffer
    buffer = StringIO()
    df.to_csv(buffer, header=False, index=False)
    buffer.seek(0)
    print(df.head())

    cursor = conn.cursor()
    try:
        cursor.copy_from(buffer, table, sep=",")
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:

        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("copy_from_stringio() done")
    cursor.close()


def data_quality_checks():
    with CursorFromConnectionPool() as cursor:
        check_load = "select count(*) from dimTeam"
        check_fact_result = "select * from factResults where home_team_id is null"
        cursor.execute(check_load)
        record_match = cursor.fetchone() is not None

        cursor.execute(check_fact_result)
        fact_check = cursor.fetchone() is None

        if record_match is False:
            print('dimTeam table is empty.')
        else:
            print('Table dimTeam is successfully populated')

        if fact_check is False:
            print('factResult table has not populated succesfully, missing ids.')
        else:
            print('Table factResult is successfully populated')

