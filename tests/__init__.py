from collections.abc import Iterable
from functools import partial
from itertools import chain
from typing import Type
from unittest import TestCase, TestLoader, TestSuite, TextTestRunner

from pynect.utils.utils import configure_logger as conf_logger

configure_logger = partial(conf_logger, project_name='pynect')


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
