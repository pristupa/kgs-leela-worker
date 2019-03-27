import psycopg2

from .settings import settings


class Cursor:
    def __init__(self, cursor):
        self._cursor = cursor

    @property
    def rowcount(self):
        return self._cursor.rowcount

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    def __del__(self):
        self._cursor.close()


class Database:
    def __init__(self):
        self._connection = None
        self.connect()
        self.execute(
            "CREATE TABLE IF NOT EXISTS leela_results ("
            "id SERIAL PRIMARY KEY,"
            "created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,"
            "game_id INTEGER NOT NULL,"
            "worker_tag TEXT DEFAULT NULL,"
            "playouts INTEGER NOT NULL,"
            "leela_result BYTEA NOT NULL,"
            "time_spent REAL NOT NULL"
            ")",
        )

    def execute(self, query, params=None):
        cursor = None
        while cursor is None:
            try:
                cursor = self._connection.cursor()
                cursor.execute(query, params)
                self._connection.commit()
            except psycopg2.OperationalError as exception:
                print(f'Exception occurred: {exception}')
                print(query)
                if cursor is not None:
                    cursor.close()
                    cursor = None
                self._connection.close()
                self.connect()

        return Cursor(cursor)

    def connect(self):
        connection = None
        print(f"Trying to connect to {settings['db_host']}...")
        while connection is None:
            try:
                connection = psycopg2.connect(
                    host=settings['db_host'],
                    database=settings['db_name'],
                    user=settings['db_user'],
                    password=settings['db_password'],
                    connect_timeout=5,
                )
            except psycopg2.OperationalError as exception:
                print(f'Failed to connect: {exception}. Trying to reconnect...')
        print('Connected.')
        self._connection = connection

    def __del__(self):
        self._connection.close()
