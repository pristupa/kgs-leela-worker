import psycopg2

from .settings import settings


class Database:
    def __init__(self):
        self._connection = psycopg2.connect(
            host=settings['db_host'],
            database=settings['db_name'],
            user=settings['db_user'],
            password=settings['db_password'],
        )
        self._cursor = self._connection.cursor()
        self._cursor.execute(
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
        self._connection.commit()

    def execute(self, query, params):
        with self._connection:
            self._cursor.execute(query, params)
        return self._cursor

    def __del__(self):
        self._cursor.close()
        self._connection.close()
