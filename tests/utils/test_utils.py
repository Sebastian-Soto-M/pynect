import time
from datetime import datetime, timedelta
from unittest import TestCase

from pynect.utils import calc_iterations, is_date_older_than_delta, split_list
from tests import configure_logger


class TestUtils(TestCase):
    date: datetime

    @classmethod
    def setUpClass(cls):
        cls.logger = configure_logger(cls.__name__)

    def setUp(self):
        t = time.time()
        self.start_time = t
        self.date = datetime.fromtimestamp(t)

    def tearDown(self):
        t: float = time.perf_counter() - self.start_time
        self.logger.debug("{:.3f}ms".format(t*1000))

    def test_is_date_older_than_delta_true(self):
        time.sleep(0.02)
        comparison = is_date_older_than_delta(
            self.date, timedelta(seconds=0.01))
        self.assertTrue(comparison)

    def test_is_date_older_than_delta_false(self):
        comparison = is_date_older_than_delta(self.date, timedelta(seconds=2))
        self.assertFalse(comparison)

    def test_calc_iterations(self):
        total_records = 100
        page_size = 10
        self.assertEqual(10, calc_iterations(total_records, page_size))

    def test_split_list(self):
        """
        Here is also an example on how to get the entire list at once

        list(split_list(initial_records, 2))
        > result: [[1, 2],[3,4],[5,6],[7,8],[9,10]]

        """
        initial_records = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        expected_result = [1, 2, 3]
        result = next(split_list(initial_records, 3))
        self.assertEqual(expected_result, result)
