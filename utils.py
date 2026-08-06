import os

import allure


def get_env_var(name):
    var = os.environ[name]
    allure.dynamic.parameter(name, var)
    return var