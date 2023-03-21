import logging
import time
from unittest import TestCase

from pynect.logging.constants import STDOUT_LOG_FORMAT


class TestCLI(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger(cls.__name__)

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        info = STDOUT_LOG_FORMAT % (TestCLI.__name__,
                                    self.id().split('.')[-1], t)
        self.logger.info(info)
