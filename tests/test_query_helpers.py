import logging
import time
from unittest import TestCase

from pynect.constants import STDOUT_LOG_FORMAT
from pynect.utils.query_helpers import RestAPIQuery


class TestQueryHelpers(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger(cls.__name__)

    def setUp(self):
        self.start_time = time.time()

    def tearDown(self):
        t = time.time() - self.start_time
        info = STDOUT_LOG_FORMAT % (TestQueryHelpers.__name__,
                                    self.id().split('.')[-1], t)
        self.logger.info(info)

    def test_simple_query(self):
        raq = RestAPIQuery('google.com')
        url = raq('api', q='demo')
        self.assertEqual(url, 'google.com/api?q=demo')

    def test_prefix_query(self):
        raq = RestAPIQuery('google.com', prefix='$')
        url = raq('api', q='demo', fq='url:*iki*')
        self.assertEqual(url, 'google.com/api?$q=demo&$fq=url:*iki*')
