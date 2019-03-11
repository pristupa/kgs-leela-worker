from pydantic import BaseSettings


class Settings(BaseSettings):
    amqp_host = 'localhost'
    amqp_user = 'kgs'
    amqp_password = 'kgs'
    db_host = 'localhost'
    db_name = 'kgs'
    db_user = 'kgs'
    db_password = 'kgs'

    class Config:
        env_prefix = 'KGS_LEELA_'


settings = Settings()
