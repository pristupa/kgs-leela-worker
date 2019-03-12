import os.path
from pydantic import BaseSettings


class Settings(BaseSettings):
    amqp_url = 'amqp://kgs:kgs@localhost/kgs'
    amqp_queue = 'kgs'
    db_host = 'localhost'
    db_name = 'kgs'
    db_user = 'kgs'
    db_password = 'kgs'
    worker_tag = 'default'
    playouts = 2000
    sgf_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sgf')

    class Config:
        env_prefix = 'KGS_LEELA_'


settings = Settings()
