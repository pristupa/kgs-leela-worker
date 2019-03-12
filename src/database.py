import psycopg2

from .settings import settings


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=settings.db_host,
            database=settings.db_name,
            user=settings.db_user,
            password=settings.db_password,
        )
        cursor = self.connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS leela_results ("
            "id SERIAL PRIMARY KEY,"
            "created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,"
            "game_id INTEGER NOT NULL,"
            "worker_tag TEXT DEFAULT NULL,"
            "playouts INTEGER NOT NULL,"
            "leela_result BYTEA NOT NULL"
            ")",
        )
        cursor.close()
        self.connection.commit()

    def close(self):
        if self.connection is not None:
            self.connection.close()
        self.connection = None
