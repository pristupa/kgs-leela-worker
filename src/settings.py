import os.path
from pydantic import BaseSettings


class Settings(BaseSettings):
    amqp_url = 'amqp://kgs:kgs@localhost/kgs'
    amqp_queue = 'kgs'
    db_url = 'postgresql://kgs:kgs@localhost/kgs'
    sgf_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sgf')

    class Config:
        env_prefix = 'KGS_LEELA_'


settings = Settings()
