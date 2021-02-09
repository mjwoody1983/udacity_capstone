import datetime as dt
import pandas as pd
from urllib.request import urlopen
import chardet
import traceback

now = dt.datetime.now()

# ***********************************************************************************
#                       VARIABLES SECTION FOR FUNCTION
# ***********************************************************************************
# leagues by season csv file contains all of the leagues that we want to load through.
url_path = 'https://www.football-data.co.uk/mmz4281/'
start_year = 2000
final_year = now.year - 1
files = open('leagues_by_season.csv')
files_to_load = files.read().split(",")
# Extra leagues, single file source - no seasons to loop
url_ext_path = 'https://www.football-data.co.uk/'
files_ext = open('extra_leagues.csv')
files_to_load_ext = files_ext.read().split(",")

# loop through each year and create season code for every season since 2000
seasons = []
for year in range(start_year, final_year):
    season_start = str(year)
    season_end = str(year + 1)
    year_url = season_start[-2:] + season_end[-2:]
    seasons.append(year_url)

# todo: Keep this for initial testing then remove
# filesLoad = ['E0.csv']
# league_path = 'https://www.football-data.co.uk/mmz4281/0001/'

arc_results = []
with open("log.txt", "w") as log:
    for files in files_to_load:
        for y in seasons:
            try:
                print(y)
                print(url_path + y + '/' + files.replace("'", ""))
                fd = urlopen(url_path + y + '/' + files.replace("'", ""))
                cDet = chardet.detect(urlopen(url_path + y + '/' + files.replace("'", "")).read())
                e_coding = cDet.get('encoding')
                df = pd.read_csv(fd, sep='delimiter', encoding=e_coding, engine='python')
                print('File loaded')
                arc_results.append(df)
            except Exception as e:
                print('logging_exception and continuing')
                file_missing = url_path + y + '/' + files.replace("'", "")
                log.write('Triggered by the following variable: ' + file_missing)
                traceback.print_exc(file=log)
                continue
frame = pd.concat(arc_results)

extra_results = []
with open("log_extra.txt", "w") as log:
    for f in files_to_load_ext:
        try:
            print(f)
            print(url_ext_path + f.replace("'", ""))
            fd = urlopen(url_ext_path + f.replace("'", ""))
            c_det = chardet.detect(urlopen(url_ext_path + f.replace("'", "")).read())
            e_coding = c_det.get('encoding')
            df = pd.read_csv(fd, sep='delimiter', encoding=e_coding, engine='python')
            print('Extra File loaded: ' + f)
            extra_results.append(df)
        except Exception as e:
            print('logging_exception and continuing')
            error_file = url_ext_path + f
            log.write('Triggered by the following variable: ' + error_file)
            traceback.print_exc(file=log)
            continue
frame_extra = pd.concat(extra_results)
print(frame_extra)

current_season = []

with open("log_extra.txt", "w") as log:
    for f in files_to_load:
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
            print(url_path + year_url + '/' + f.replace("'", ""))
            fd = urlopen(url_path + year_url + '/' + f.replace("'", ""))
            c_det = chardet.detect(urlopen(url_path + year_url + '/' + f.replace("'", "")).read())
            e_coding = c_det.get('encoding')
            df = pd.read_csv(fd, sep='delimiter', encoding=e_coding, engine='python')
            print('Extra File loaded: ' + f)
            current_season.append(df)
        except Exception as e:
            print('logging_exception and continuing')
            error_file = url_path + year_url + '/' + f.replace("'", "")
            log.write('Triggered by the following variable: ' + error_file)
            traceback.print_exc(file=log)
            continue
frame_extra = pd.concat(current_season)
print(frame_extra)




