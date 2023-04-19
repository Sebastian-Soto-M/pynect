from tests.utils.test_query_helpers import TestQueryHelpers

from .test_cli import TestCLI
from .test_decorators import TestTimeitDecorator
from .test_utils import TestUtils

TESTS = {TestCLI, TestQueryHelpers, TestTimeitDecorator, TestUtils}
