import logging

from sys import stdout
import pynect.constants as pc

logging.basicConfig(level=logging.INFO, stream=stdout,
                    format=pc.FILE_LOG_FORMAT, encoding='utf-8')
