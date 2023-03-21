from collections.abc import Iterable
from typing import Type
from unittest import TestCase, TestSuite, TextTestRunner, TestLoader
from itertools import chain
from .test_query_helpers import TestQueryHelpers


def get_suite(*tests: Iterable[Type[TestCase]]) -> TestSuite:
    suites = [TestLoader().loadTestsFromTestCase(test)
              for test in chain(*tests)]
    return TestSuite(suites)


if __name__ == "__main__":  # pragma: no cover
    TextTestRunner().run(get_suite([TestQueryHelpers]))
