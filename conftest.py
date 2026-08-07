import allure
import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")

        if page:
            allure.attach(
                page.screenshot(),
                attachment_type=allure.attachment_type.PNG
            )