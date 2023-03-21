import logging
from collections.abc import Iterable
from itertools import chain
from sys import stdout
from typing import Type
from unittest import TestCase, TestLoader, TestSuite, TextTestRunner

import pynect.logging.constants as pc


def _build_suite(
    loader: TestLoader, *test_classes: Iterable[Type[TestCase]]
) -> TestSuite:
    test_suite = TestSuite()
    test_suite.addTests(
        map(loader.loadTestsFromTestCase, chain(*test_classes)))
    return test_suite


def run(*test_classes) -> TestSuite:
    loader = TestLoader()
    TextTestRunner().run(_build_suite(loader, *test_classes))


logging.basicConfig(level=logging.INFO, stream=stdout,
                    format=pc.FILE_LOG_FORMAT, encoding='utf-8')
