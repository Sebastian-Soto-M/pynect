from unittest import TestCase

from pynect.utils.query_helpers import RestAPIQuery


class TestQueryHelpers(TestCase):

    def test_simple_query(self):
        raq = RestAPIQuery('google.com')
        url = raq('api', q='demo')
        self.assertEqual(url, 'google.com/api?q=demo')

    def test_suffix_query(self):
        raq = RestAPIQuery('google.com', suffix='$')
        url = raq('api', q='demo', fq='url:*iki*')
        self.assertEqual(url, 'google.com/api?q=demo$&fq=url:*iki*$')

    def test_prefix_query(self):
        raq = RestAPIQuery('google.com', prefix='$')
        url = raq('api', q='demo', fq='url:*iki*')
        self.assertEqual(url, 'google.com/api?$q=demo&$fq=url:*iki*')

    def test_default_query(self):
        host = 'google.com'
        query = RestAPIQuery(host)()
        self.assertEqual(host, query)
