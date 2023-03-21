import logging
from collections.abc import Iterable
from itertools import chain
from sys import stdout
from typing import Type
from unittest import TestCase, TestLoader, TestSuite, TextTestRunner

import pynect.constants as pc


def _build_suite(
    loader: TestLoader, *test_classes: Iterable[Type[TestCase]]
) -> TestSuite:
    suites_list = []
    for test_class in chain(*test_classes):
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)
    return TestSuite(suites_list)


def run(*test_classes) -> TestSuite:
    loader = TestLoader()
    TextTestRunner().run(_build_suite(loader, *test_classes))


logging.basicConfig(level=logging.INFO, stream=stdout,
                    format=pc.FILE_LOG_FORMAT, encoding='utf-8')
