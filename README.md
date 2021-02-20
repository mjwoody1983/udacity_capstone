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
* Historic results for 22 European Leagues from 28 seasons. Data is supplied in CSV format. https://www.football-data.co.uk/data.php
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
The data model contains five different data sources that are loaded into staging, these tables are then 
distributed into six dimension tables and two fact tables. The dimension tables breakout the data from the 
different sources breaking down into the following:

#### Dimension Table
* dimBookmaker - Distinct list of bookmakers where odds are available. Primary KEY = bookmaker_id
* dimDate - Distinct list of dates available in the data, going back 28 years. Primary Key = date_id  
* dimFixture - Distinct list of all fixtures in the data. PK = fixture_id
* dimLeague - Distinct list of all league in the data. PK = league_id
* dimSeason - All season available in the data going back 28 years. PK = season_id
* dimTeam - All teams available within the data. PK = team_id

#### Fact Table
* factOdds - Contains all odds results in the data to be analysed.
* factResults - Contains all results data over 28 seasons including present season to be analysed.

#### Purpose
The purpose of this data model is to allow the end user to start to analyse and draw conclusions
on future sporting events and bookmaker prices based on historical trends. 

#### Choice of technology and data model
For this project I choose a traditional RDBMS data warehouse approach for a number of reasons:
* Data warehouse helps reduce total turnaround time for analysis and reporting.
* Provides a clean enviroment for analysts to work in, focusing on the results rather than pulling together complex queries.
* Data is standardised improving quality and consistency.
* provides an audit trail of where, when and how the data was loaded and allows data tracking.
* Scalability: If you have volumes of historical data that need consolidation, a data warehouse makes for easy access in a common place, with the ability to scale in the future.
* NoSQL wasn't an option as need the ability to perform analytical queries at a later date.
* Postgres is cheaper than Redshift, considering this data is going to be used as an edge on the sportbooks, any additional costs impact margin.

### Data Quality
Quality checks were incorporated into the ETL process.

* Fixtures insert checks whether the fixture has been loaded alredy, if it already exists it will skip the load step and return a line comment stating "Records already exists for this fixture".
* All insert statements for the dimension and fact tables check if the record already exists, if it does this record will not be loaded. For example, if Liverpool are already loaded in dimTeam this will not insert them again.
* Final data quality checks test that there are no blank ids in the fact table and that another of the dimension tables is not empty. These quality checks can be expanded.

### Project steps
* Sourced all data sources, signed up to oddschecker to obtain API key.
* Developed use case.
* Looked into data formats, scale, and looked into sample downloads.
* Identified data model and how to combine the data.
* Spun up Postgres RDBMS instance on AWS. Changed parameter group for DB to ensure free tier wasn't losing space to excessive logging.
* Created the scripts for table creation.  
* Developed and tested the extraction process.
* Looked into AWS Lambda and how the extract process would work.
* Developed and tested the transform process. Using pandas, database connection, loading the data in the most efficient way.
* Ran multiple tests, fixes, odds data running every 10 minutes to test volume loading.
* Ran final test queries to ensure table creation and database performance. All queries return in seconds.

### Enviroment
* USER=
* PASSWORD=
* DATABASE=
* HOST=
* api_key=




### Other scenarios
If the database size was increased by 100X, query performance should still be fine although it might be time to start planning some alternative solutions. In this case it would be worth considering moving to either Redshift or Snowflake, this would cope with the larger data volumes and ensure support for aggregate trend analysis. 

To update the database every morning at 7am, it would make sense to utilize a pipeline scheduling application such as Airflow although I would probably use Lambda functions. Lambda comes with a lot of monitoring, is easy to use and is flexible across different enviroments. It comes with monitoring and logging so any errors can be seen from the summary dashboard, alarms can also be set triggering alerts. 

Postgres can cope with 100 connections, the default is typically set to 100 connections. At this point if there were more needed it might mean we need to scale up our deployment, more importantly at this point would be analysing the use case and providing the end user with the correct tools to work with the data. For example a well written app typically doesn't need a large number of connections.


