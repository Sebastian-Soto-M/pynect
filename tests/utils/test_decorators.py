import logging
import time
import unittest

from pynect.utils import timeit
from tests import configure_logger


class TestTimeitDecorator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.logger = configure_logger(__name__, logging.DEBUG)

    def test_decorator_with_logging(self):
        # Define a test function
        @timeit(logger=self.logger, level=logging.DEBUG)
        def test_function():
            time.sleep(0.1)

        # Call the decorated function and capture the log output
        with self.assertLogs(level='DEBUG') as logs:
            test_function()
        # Assert that the log output contains the expected message
        self.assertIn('test_function took', logs.output[0])
    #
    # def test_decorator_without_logging(self):
    #     # Define a test function
    #     @timeit()
    #     def test_function():
    #         time.sleep(0.1)
    #
    #     # Call the decorated function and ensure it runs without errors
    #     test_function()
