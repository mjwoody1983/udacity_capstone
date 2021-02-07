import datetime as dt
import pandas as pd
from urllib.request import urlopen
import chardet

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


for files in files_to_load:
    for y in seasons:
        print('files is: ' + files + ' season is: ' + y)

# fd = urlopen('https://www.football-data.co.uk/mmz4281/2021/e0.csv')
# print(type(fd))
# print(chardet.detect(fd.read()))

