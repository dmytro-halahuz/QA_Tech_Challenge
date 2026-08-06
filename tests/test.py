import playwright
import pytest

from utils  import get_env_var

fashionhub_base_url = get_env_var('BASE_URL')

def test_check_console():
    print(fashionhub_base_url)

