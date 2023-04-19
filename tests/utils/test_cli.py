import time
from unittest import TestCase

from tests import configure_logger


class TestCLI(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.logger = configure_logger(cls.__name__)

    def setUp(self):
        self.start_time = time.time()

    def tearDown(self):
        t: float = time.perf_counter() - self.start_time
        self.logger.info("{:.3f}ms".format(t*1000))
