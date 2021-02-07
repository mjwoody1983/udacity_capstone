import datetime as dt
import pandas as pd
from urllib.request import urlopen
import chardet
import traceback

now = dt.datetime.now()

# leagues by season csv file contains all of the leagues that we want to load through.
url_path = 'https://www.football-data.co.uk/mmz4281/'
start_year = 2000
final_year = now.year - 1
files = open('leagues_by_season.csv')
files_to_load = files.read().split(",")
url_path = 'https://www.football-data.co.uk/mmz4281/'

# loop through each year and create season code for every season since 2000
seasons = []
for year in range(start_year, final_year):
    season_start = str(year)
    season_end = str(year + 1)
    year_url = season_start[-2:] + season_end[-2:]
    seasons.append(year_url)

filesLoad = ['E0.csv']
league_path = 'https://www.football-data.co.uk/mmz4281/0001/'

arcResults = []
list_ = []
with open("log.txt", "w") as log:
    for files in files_to_load:
        for y in seasons:
            try:
                print(y)
                print(url_path + y + '/' + files.replace("'", ""))
                fd = urlopen(url_path + y + '/' + files.replace("'", ""))
                cDet = chardet.detect(urlopen(url_path + y + '/' + files.replace("'", "")).read())
                e_coding = cDet.get('encoding')
                # print(e_coding)
                df = pd.read_csv(fd, sep='delimiter', header=None, encoding=e_coding, engine='python')
                print('File loaded')
                arcResults.append(df)
            except Exception as e:
                print('logging_exception and continuing')
                traceback.print_exc(file=log)
                continue
frame = pd.concat(arcResults)



#
# for files in filesLoad:
#     for y in range(1,5):
#         print(y)
#         fd = urlopen(league_path + files)
#         df = pd.read_csv(fd, encoding='ascii')
#         list_.append(df)
# frame = pd.concat(list_)
# print(list_)