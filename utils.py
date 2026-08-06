import os
import allure

def get_env_var(name, hidden=False):
    var = os.environ[name]
    if hidden:
        allure.dynamic.parameter(name, var, mode=allure.parameter_mode.MASKED)
    else:
        allure.dynamic.parameter(name, var)

    return var