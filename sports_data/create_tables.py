from sports_data.database_connection import Database
from sports_data.database_connection import CursorFromConnectionPool
from sports_data.sql_queries import create_table_queries, insert_table_queries, drop_tbl

Database.initialise()


def create_tables():
    """
    Creates each table using the queries in `create_table_queries` list.
    """
    for query in create_table_queries:
        with CursorFromConnectionPool() as cursor:
            print(query)
            cursor.execute(query)


def insert_dim_records():
    """
    Inserts into each table using the queries in `insert_table_queries` list.
    """
    for query in insert_table_queries:
        with CursorFromConnectionPool() as cursor:
            print(query)
            cursor.execute(query)

def drop_tables():
    """
    Drop tables when finished with the project.
    """
    for query in drop_tbl:
        with CursorFromConnectionPool() as cursor:
            print(query)
            cursor.execute(query)

def main():
    create_tables()


if __name__ == "__main__":
    main()
