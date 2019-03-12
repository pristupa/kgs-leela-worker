import sys
from logging import Logger
from logging import StreamHandler

logger = Logger('kgs')
logger.addHandler(StreamHandler(sys.stdout))
