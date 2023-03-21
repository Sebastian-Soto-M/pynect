from tests import run
from tests.utils import TESTS as UTILS_TESTS
from tests.api import TESTS as API_TESTS


if __name__ == "__main__":  # pragma: no cover
    run(UTILS_TESTS, API_TESTS)
