import configparser
import os.path

_config = configparser.ConfigParser()
_config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

settings = _config['kgs-leela-worker']
