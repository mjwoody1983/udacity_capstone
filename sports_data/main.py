from sports_data.create_tables import *
from sports_data.loading_data import *


def main():
    # Create initial staging, dimension and fact tables
    create_tables()

    # Dataframes to hold the data to process
    df = process_extra_results()
    df2 = process_history_results()

    # Connect to the database and load the data at each step.
    conn = connect(param_dic)
    copy_from_stringio(conn, df, 'staging_additional_leagues')  # copy the dataframe to SQL
    copy_from_stringio(conn, df2, 'staging_historic_data')
    odds_df = odds_api_data()
    copy_from_stringio(conn, odds_df, 'staging_odds_data_raw')
    process_fixture_data()
    process_current_season()
    conn.close()

    # Insert the data from staging into the dimension tables
    insert_dim_records()

    # Do some final data quality checks.
    data_quality_checks()

if __name__ == "__main__":
    main()
