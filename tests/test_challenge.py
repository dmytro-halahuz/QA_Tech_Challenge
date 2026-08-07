import allure
import requests

from models.pages import HomePage, AboutPage, LoginPage, GithubPRsPage
import pytest_check as check
from urllib.parse import urljoin

from utils import get_env_var, TempCSVFile

@allure.title("Verify Home page has no console errors")
def test_check_console_on_home(page):
    home_page = HomePage(page)
    home_page.listen_for_console_errors()
    home_page.navigate()

    with allure.step(f"Verify no console errors are present"):
        assert home_page.console_errors == []

@allure.title("Verify About page has no console errors")
def test_check_console_on_about(page):
    about_page = AboutPage(page)
    about_page.listen_for_console_errors()
    about_page.navigate()

    with allure.step(f"Verify no console errors are present"):
        assert about_page.console_errors == []


@allure.title("Check all links on the Home page")
def test_links_on_home(page):
    home_page = HomePage(page)
    home_page.navigate()

    link = page.locator("a")

    hrefs = []
    for i in range(link.count()):
        hrefs.append(link.nth(i).get_attribute('href'))

    for href in hrefs:
        with allure.step(f"Check if '{href}' returns 200 or 30x status code"):
            url = urljoin(home_page.url, href)
            response = page.goto(url)
            status = str(response.status)
            check.is_true(status == '200' or status.startswith('30'),f"link: {href}, status: {status}")

@allure.title("Log in to FashionHub")
def test_login(page):
    username = get_env_var('USERNAME')
    password = get_env_var('PASSWORD', True)

    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(username, password).verify_account(username)

@allure.title("Get a list of pull requests")
def test_get_pull_requests():
    owner = "appwrite"
    repo = "appwrite"

    csv_file = TempCSVFile('Open Pull Requests')
    csv_file.writerow(["Name", "Created Date", "Author"])

    page = 1

    while True:
        pull_requests = get_pull_requests(owner, repo, page)

        if not pull_requests:
            break

        for pr in pull_requests:
            csv_file.writerow([pr['title'], pr['created_at'], pr['user']['login']])

        page += 1

    csv_file.attach_to_report()

@allure.title("Get a list of pull requests")
def test_get_pull_requests(page):
    owner = "appwrite"
    repo = "appwrite"

    csv_file = TempCSVFile('Open Pull Requests')
    csv_file.writerow(["Name", "Created Date", "Author"])

    pr_page = GithubPRsPage(page, owner, repo)
    pr_page.navigate()

    while True:
        csv_file.writerows(pr_page.get_prs())
        if not pr_page.next_page():
            break

    csv_file.attach_to_report()

@allure.title("Get a list of pull requests")
def test_get_pull_requests_api():
    owner = "appwrite"
    repo = "appwrite"

    csv_file = TempCSVFile('Open Pull Requests')
    csv_file.writerow(["Name", "Created Date", "Author"])

    page = 1

    while True:
        pull_requests = get_pull_requests(owner, repo, page)

        if not pull_requests:
            break

        for pr in pull_requests:
            csv_file.writerow([pr['title'], pr['created_at'], pr['user']['login']])

        page += 1

    csv_file.attach_to_report()

def get_pull_requests(owner, repo, page, state=open, per_page=100, ):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    token = get_env_var('GITHUB_TOKEN')

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {token}",
    }

    params = {
        "state": state,
        "per_page": per_page,
        "page": page
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response.json()