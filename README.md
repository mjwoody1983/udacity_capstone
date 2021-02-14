# Data Engineering - Sports Data
## Postgres Data Warehouse

### Overview
This project creates a sports and betting data warehouse, this combines historical results information from
20 seasons across Europe. There is additional results data from historic seasons in South America, North America, Russia etc.
Also loaded are the current seasons results, upcoming fixtures and current odds associated with those matches.

The second source of data comes from Odds Checker API, this provides a list of current in-season sports as well as returning a list of upcoming and live games with recent odds for a given sport, region and market.

The current scope of the project focuses initially on Football(Soccer), but will expand to Tennis, NFL, MLB and Cricket. 

### Data Sources
#### Historic Results and Fixtures
* Historic results for 22 European Leagues from 25 seasons. Data is supplied in CSV format. https://www.football-data.co.uk/data.php
* Current Season results across 22 European leagues. Data is supplied in CSV format. https://www.football-data.co.uk/data.php
* Additional leagues; data for 16 other worldwide premier divisions, with fulltime results and closing match odds (best and average market price, and Pinnacle odds) dating back to 2012/13. https://www.football-data.co.uk/data.php
* Fixtures and betting odds for upcoming games, collected Friday afternoons for weekend fixtures, and on Tuesday afternoons for midweeek games. https://www.football-data.co.uk/data.php

#### Bookmaker Odds
Bookmaker odds across a number of the major sports, covering a significant portion of bookmakers to provide a picture of the market. List of bookmakers available can be found here: https://the-odds-api.com/sports-odds-data/bookmaker-apis.html.

The API provides odds data for the following in-season sports:
* Football odds data   NFL, College Football (NCAA), Aussie Rules (AFL)
* Soccer odds data   EPL, FA Cup, German Bundesliga, UEFA Europa & Champions Leagues, Italian Serie A, Spanish La Liga, Campeonato Brasileiro Série A, A-league and much more
* Basketball odds data   NBA, US College Basketball (NCAA), Euroleague
* Baseball odds data   MLB
* Ice hockey odds data   NHL
* Cricket odds data   Test matches, IPL, Big Bash and more
* Rugby league odds data   Aussie NRL
* Golf odds data   Masters Tournament, PGA Championship, US Open, The Open Championship
* Tennis odds data   All Grand Slams
* Politics odds data   Next US President odds
 
...and the following betting markets:
* head-to-head (moneyline) odds
* point spreads (handicap) odds on version 3+
* totals (over/under) odds on version 3+
* outrights (futures) odds on version 3+ for relevant sports. Outrights are futures markets, cover Super Bowl Winner, Golf Majors etc.

##### API Host
All requests use the host https://api.the-odds-api.com

###### GET sports
Returns a list of in-season sport objects.

Endpoint: GET /v3/sports/?apiKey={apiKey}

###### GET odds
Returns a list of upcoming and live games with recent odds for a given sport, region and market

Endpoint: GET /v3/odds/?apiKey={apiKey}&sport={sport}&region={region}&mkt={mkt}

### Data Model
