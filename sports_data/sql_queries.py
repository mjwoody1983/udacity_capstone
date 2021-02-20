fixtures_create_table = ("""
    create table if not exists staging_fixtures (
            league          text,
            fixture_date    text,
            fixture_time    text,
            home_team       text,
            away_team       text,
            b365h           numeric,
            b365d           numeric,
            b365a           numeric,
            bwh             numeric,
            bwd             numeric,
            bwa             numeric,
            iwh             numeric,
            iwd             numeric,
            iwa             numeric,
            psh             numeric,
            psd             numeric,
            psa             numeric,
            whh             numeric,
            whd             numeric,
            wha             numeric,
            vch             numeric,
            vcd             numeric,
            vca             numeric,
            best_home_price numeric,
            best_draw_price numeric,
            best_away_price numeric,
            avg_home_price  numeric,
            avg_draw_price  numeric,
            avg_away_price  numeric
    )

""")

current_season_data = ("""
    create table if not exists staging_current_season (
            season          text,
            league          text,
            fixture_date    text,
            fixture_time    text,
            home_team       text,
            away_team       text,
            fthg            text,
            ftag            text,
            ftr             text,
            hthg            text,
            htag            text,
            htr             text,
            referee         text,
            hs              text,
            aways           text,
            hst             text,
            ast             text,
            hf              text,
            af              text,
            hc              text,
            ac              text,
            hy              text,
            ay              text,
            hr              text,
            ar              text,
            b365h           text,
            b365d           text,
            b365a           text,
            bwh             text,
            bwd             text,
            bwa             text,
            iwh             text,
            iwd             text,
            iwa             text,
            psh             text,
            psd             text,
            psa             text,
            whh             text,
            whd             text,
            wha             text,
            vch             text,
            vcd             text,
            vca             text,
            best_home_price text,
            best_draw_price text,
            best_away_price text,
            avg_home_price  text,
            avg_draw_price  text,
            avg_away_price  text,
            created_utc     timestamp
);
""")

additional_season_data = ("""
    create table if not exists staging_additional_leagues (
                    country_name    text,
                    league          text,
                    rel_season      text,
                    fixture_date    text,
                    fixture_time    text,
                    home_team       text,
                    away_team       text,
                    hg              text,
                    ag              text,
                    match_res       text,
                    ph              text,
                    pd              text,
                    pa              text,
                    best_home_price text,
                    best_draw_price text,
                    best_away_price text,
                    avg_home_price  text,
                    avg_draw_price  text,
                    avg_away_price  text,
                    created_date    timestamp
    )
""")

historic_season_data = ("""
    create table if not exists staging_historic_data (
            season          text,
            league          text,
            fixture_date    text,
            fixture_time    text,
            home_team       text,
            away_team       text,
            fthg            text,
            ftag            text,
            ftr             text,
            hthg            text,
            htag            text,
            htr             text,
            hs              text,
            aways           text,
            b365h           text,
            b365d           text,
            b365a           text,
            bwh             text,
            bwd             text,
            bwa             text,
            iwh             text,
            iwd             text,
            iwa             text,
            psh             text,
            psd             text,
            psa             text,
            whh             text,
            whd             text,
            wha             text,
            vch             text,
            vcd             text,
            vca             text,
            best_home_price text,
            best_draw_price text,
            best_away_price text,
            avg_home_price  text,
            avg_draw_price  text,
            avg_away_price  text,
            created_utc     timestamp
    )
""")

odds_checker_raw = ("""
    create table if not exists staging_odds_data_raw(
        league             varchar(100),
        team_0             varchar(50),
        team_1             varchar(50),
        kick_off_epoch     integer,
        kick_off_timestamp timestamp,
        home_team          varchar(75),
        bookmaker          varchar(75),
        odds_0             numeric,
        odds_1             numeric,
        odds_2             numeric,
        odds_o_or          numeric,
        odds_1_or          numeric,
        odds_2_or          numeric,
        bookmaker_margin   numeric,
        stripped_0         numeric,
        stripped_1         numeric,
        stripped_2         numeric,
        target_0           numeric,
        target_1           numeric,
        target_2           numeric,
        created_date       timestamp
    )
""")

dimbookmaker_create_table = ("""
    create table if not exists dimbookmaker
        (
            bookmaker_id serial not null
                constraint bookmaker_pk
                    primary key,
            bookmaker    text
        );

""")

dimdate_create_table = ("""
    create table if not exists dimdate
        (
            date_id      serial not null
                constraint date_pk
                    primary key,
            fixture_date date,
            fix_dt       text
        );
""")

dimfixture_create_table = ("""
    create table if not exists dimfixture
        (
            fixture_id   serial not null
                constraint fixture_pk
                    primary key,
            league_id    integer,
            date_id      integer,
            home_team_id integer,
            away_team_id integer,
            b365h        integer,
            b365d        integer,
            b365a        integer
        );
""")

dimleague_create_table = ("""
    create table if not exists dimleague
        (
            league_id serial not null
                constraint league_pk
                    primary key,
            league    text
        );
""")

dimseason_create_table = ("""
    create table if not exists dimseason
        (
            season_id serial not null
                constraint season_pk
                    primary key,
            season    text
        );
""")

dimteam_create_table = ("""
    create table if not exists dimteam
        (
            team_id serial not null
                constraint team_pk
                    primary key,
            team    text
        );
""")

factodds_create_table = ("""
    create table if not exists factodds
        (
            odds_id          serial not null
                constraint odds_id_pk
                    primary key,
            home_team_id     integer,
            away_team_id     integer,
            bookmaker_id     integer,
            odds_home        numeric,
            odds_draw        numeric,
            odds_away        numeric,
            odds_target_home numeric,
            odds_target_draw numeric,
            odds_target_away numeric
        );
""")

factresults_create_table = ("""
    create table if not exists factresults
        (
            record_id       serial not null
                constraint record_id_pk
                    primary key,
            season_id       integer,
            league_id       integer,
            date_id         integer,
            home_team_id    integer,
            away_team_id    integer,
            fthg            numeric,
            ftag            numeric,
            ftr             text,
            hthg            numeric,
            htag            numeric,
            htr             text,
            hs              numeric,
            aways           numeric,
            b365h           numeric,
            b365d           numeric,
            b365a           numeric,
            best_home_price numeric,
            best_draw_price numeric,
            best_away_price numeric,
            avg_home_price  numeric,
            avg_draw_price  numeric,
            avg_away_price  numeric
        );
""")
# Insert records
fixtures_insert = ("""
    INSERT INTO staging_fixtures VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
     )
""")

current_season_insert = ("""
    INSERT INTO staging_current_season VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                                  %s, %s, %s, %s, %s, %s, %s, %s, now()
                                                    
     )
""")

dimBookmaker_insert = ("""
    insert into dimBookmaker (bookmaker)
        select distinct odr.bookmaker
        from staging_odds_data_raw odr
        left join dimbookmaker d on odr.bookmaker = d.bookmaker
        where d.bookmaker_id is null;
""")

dimDate_insert = ("""
    insert into dimDate (fixture_date, fix_dt)
        select distinct ad.fixture_date, ad.fix_dt
        from (
                 select distinct to_date(fixture_date, 'dd/mm/yyyy') fixture_date, fixture_date fix_dt
                 from staging_fixtures
                 union all
                 select distinct to_date(fixture_date, 'dd/mm/yyyy') fixture_date, fixture_date fix_dt
                 from staging_current_season
                 union all
                 select distinct to_date(fixture_date, 'dd/mm/yyyy') fixture_date, fixture_date fix_dt
                 from staging_additional_leagues
                 union all
                 select distinct case
                                     when length(fixture_date) = 8 then to_date(fixture_date, 'dd/mm/yy')
                                     else to_date(fixture_date, 'dd/mm/yyyy') end fixture_date,
                                 fixture_date                                     fix_dt
                 from staging_historic_data
             ) ad
        left join dimDate dd on dd.fix_dt = ad.fix_dt
        where dd.date_id is null;

""")

dimFixture_insert = ("""
    insert into dimFixture (league_id, date_id, home_team_id, away_team_id, b365h, b365d, b365a)
        select dl.league_id,
               d.date_id,
               dth.team_id,
               dta.team_id,
               f.b365h,
               f.b365d,
               f.b365a
        from staging_fixtures f
                 join dimLeague dl on f.league = dl.league
                 join dimTeam dth on f.home_team = dth.team
                 join dimTeam dta on f.away_team = dta.team
                 join dimDate d on f.fixture_date = d.fix_dt
                 left join dimFixture dF on d.date_id = dF.date_id and df.home_team_id = dth.team_id and df.away_team_id = dta.team_id
        where df.league_id is null;
""")

dimLeague_insert = ("""
    insert into dimLeague (league)
        select distinct d.league
        from (
                 select distinct league
                 from staging_current_season
                 union all
                 select distinct league
                 from staging_additional_leagues
             ) d
        left join dimLeague dl on d.league = dl.league
        where dl.league_id is null;
;
""")

dimSeason_insert = ("""
    insert into dimSeason (season)
        select distinct s.season
        from (
                 select distinct season
                 from staging_current_season
                 union all
                 select distinct season
                 from staging_historic_data
        ) s
        left join dimSeason ds on ds.season = s.season
        where ds.season_id is null;
""")

dimTeam_insert = ("""
insert into dimTeam (team)
        select distinct t.team
        from (
                 select distinct home_team team, league
                 from staging_current_season
                    union all
                 select distinct away_team team, league
                 from staging_current_season
                    union all
                 select distinct home_team team, league
                 from staging_historic_data
                    union all
                 select distinct away_team team, league
                 from staging_historic_data
                    union all
                 select distinct home_team, league
                 from staging_additional_leagues
                    union all
                 select distinct away_team, league
                 from staging_additional_leagues
                    union all
                 select distinct team_0, league
                 from staging_odds_data_raw
                    union all
                 select distinct team_1, league
                 from staging_odds_data_raw
             ) t
            left join dimTeam dt on t.team = dt.team
            where dt.team_id is null;
""")

factOdds_insert = ("""
    insert into factOdds (home_team_id, away_team_id, bookmaker_id, odds_home, odds_draw, odds_away, odds_target_home, odds_target_draw, odds_target_away)
        select dt.team_id,
               dta.team_id,
               d.bookmaker_id,
               odds_0,
               odds_1,
               odds_2,
               target_0,
               target_1,
               target_2
        from staging_odds_data_raw odr
        join dimTeam dt on odr.home_team = dt.team
        join dimTeam dta on odr.home_team = dta.team
        join dimbookmaker d on odr.bookmaker = d.bookmaker
        where created_date > now()::date - interval '1 hours';
""")

factResults_insert = ("""
    insert into factResults (season_id, league_id, date_id, home_team_id, away_team_id, fthg, ftag, ftr, hthg, htag, htr, hs, aways, b365h, b365d, b365a, best_home_price, best_draw_price, best_away_price, avg_home_price, avg_draw_price, avg_away_price)
        select ds.season_id,
               dl.league_id,
               dd.date_id,
               dth.team_id home_team_id,
               dta.team_id away_team_id,
               case when hr.fthg = '' then null else hr.fthg::decimal end,
               case when hr.fthg = '' then null else hr.ftag::decimal end,
               hr.ftr,
               case when hr.hthg = '' then null else hr.hthg::numeric end,
               case when hr.htag = '' then null else hr.htag::numeric end,
               hr.htr,
               case when hr.hs = '' then null else hr.hs::numeric end,
               case when hr.aways = '' then null else hr.aways::numeric end,
               case when hr.b365h = '' then null else hr.b365h::numeric end b365h,
               case when hr.b365d = '' then null else hr.b365d::numeric end b365d,
               case when hr.b365a = '' then null else hr.b365a::numeric end b365a,
               case when hr.best_home_price = '' then null else hr.best_home_price::numeric end best_home_price,
               case when hr.best_draw_price = '' then null else hr.best_draw_price::numeric end best_draw_price,
               case when hr.best_away_price = '' then null else hr.best_away_price::numeric end best_away_price,
               case when hr.avg_home_price = '' then null else hr.avg_home_price::numeric end avg_home_price,
               case when hr.avg_draw_price = '' then null else hr.avg_draw_price::numeric end avg_draw_price,
               case when hr.avg_away_price = '' then null else hr.avg_away_price::numeric end avg_away_price
        from (
                 select season,
                        league,
                        fixture_date,
                        home_team,
                        away_team,
                        fthg,
                        ftag,
                        ftr,
                        hthg,
                        htag,
                        htr,
                        hs,
                        aways,
                        b365h,
                        b365d,
                        b365a,
                        best_home_price,
                        best_draw_price,
                        best_away_price,
                        avg_home_price,
                        avg_draw_price,
                        avg_away_price
                 from staging_historic_data
                 union all
                 select season,
                        league,
                        fixture_date,
                        home_team,
                        away_team,
                        fthg,
                        ftag,
                        ftr,
                        hthg,
                        htag,
                        htr,
                        hs,
                        aways,
                        b365h,
                        b365d,
                        b365a,
                        best_home_price,
                        best_draw_price,
                        best_away_price,
                        avg_home_price,
                        avg_draw_price,
                        avg_away_price
                 from staging_current_season
                 union all
                 select left(right(rel_season, 7), 2) || right(rel_season, 2),
                        league,
                        al.fixture_date,
                        al.home_team,
                        al.away_team,
                        hg,
                        ag,
                        match_res,
                        null::text hthg,
                        null::text htag,
                        null::text htr,
                        null::text hs,
                        null::text aways,
                        ph,
                        pd,
                        pa,
                        best_home_price,
                        best_draw_price,
                        best_away_price,
                        avg_home_price,
                        avg_draw_price,
                        avg_away_price
                 from staging_additional_leagues al
             ) hr
        join dimSeason ds on hr.season = ds.season
        join dimLeague dl on hr.league = dl.league
        join dimTeam dth on hr.home_team = dth.team
        join dimTeam dta on hr.away_team = dta.team
        left join dimDate dd on hr.fixture_date = dd.fix_dt
        left join factResults fr on fr.date_id = dd.date_id and dth.team_id = fr.home_team_id and dta.team_id = fr.away_team_id
        where fr.record_id is null;
""")

drop_tbl = ("""
    drop table dimbookmaker;
    drop table dimdate;
    drop table dimfixture;
    drop table dimleague;
    drop table dimseason;
    drop table dimteam;
    drop table factodds;
    drop table factresults;
    drop table staging_additional_leagues;
    drop table staging_current_season;
    drop table staging_fixtures;
    drop table staging_historic_data;
    drop table staging_odds_data_raw;
    
""")

create_table_queries = [fixtures_create_table, current_season_data, additional_season_data, historic_season_data,
                        odds_checker_raw, dimbookmaker_create_table,
                        dimdate_create_table, dimfixture_create_table, dimleague_create_table, dimseason_create_table,
                        dimteam_create_table, factodds_create_table,
                        factresults_create_table]

insert_table_queries = [dimBookmaker_insert, dimDate_insert, dimFixture_insert, dimLeague_insert, dimSeason_insert,
                        dimTeam_insert,
                        factOdds_insert, factResults_insert]

drop_table_queries = [drop_tbl]
