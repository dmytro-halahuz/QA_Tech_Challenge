import playwright
import pytest

from utils import get_env_var

@pytest.fixture(scope="session")
def base_url():
    return get_env_var('BASE_URL')

def test_check_console(base_url):
    print(base_url)

