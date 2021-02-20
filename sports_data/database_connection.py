from psycopg2 import pool
from decouple import config


class Database:
    __connection_pool = None

    @classmethod
    def initialise(cls):
        cls.__connection_pool = pool.SimpleConnectionPool(1,
                                                          10,
                                                          database=config('DATABASE'),
                                                          user=config('USER'),
                                                          password=config('PASSWORD'),
                                                          host=config('HOST')
                                                          )

    @classmethod
    def get_connection(cls):
        print('get_connection')
        return cls.__connection_pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        Database.__connection_pool.putconn(connection)

    @classmethod
    def close_all_connection(cls):
        print('connection closed')
        Database.__connection_pool.closeall()


class CursorFromConnectionPool:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        print('close_connection')
        Database.return_connection(self.connection)
