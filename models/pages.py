import allure
import playwright.async_api
from playwright.sync_api import expect
from utils import get_env_var

class BasePage:
    def __init__(self, page):
        self.page = page
        self.url = get_env_var('BASE_URL')
        self.console_errors = []

    def listen_for_console_errors(self):
        self.page.on("console", lambda msg: self.console_errors.append(msg.text)
        if msg.type == "error" else None)

    def get_console_errors(self):
        return self.console_errors

    def navigate(self):
        with allure.step('Navigate to ' + self.__class__.__name__):
            self.page.goto(self.url)

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.header = page.locator("div > h1")

    def navigate(self):
        super().navigate()
        expect(self.header).to_be_visible()
        expect(self.header).to_have_text('Welcome to FashionHub')

class AboutPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url += '/about.html'
        self.header = page.locator("div > h1")

    def navigate(self):
        super().navigate()
        expect(self.header).to_be_visible()
        expect(self.header).to_have_text('About FashionHub')

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url += '/login.html'
        self.header = page.locator("#loginPanel > h2")
        self.username = page.locator("#username")
        self.password = page.locator("#password")
        self.loginButton = page.locator("#loginForm > input[type='submit']")

    def navigate(self):
        super().navigate()
        expect(self.header).to_be_visible()
        expect(self.header).to_have_text('Login to FashionHub')

    def login(self, username, password):
        with allure.step(f"Log in as '{username}'"):
            self.username.fill(username)
            self.password.fill(password)
            self.loginButton.click()
            return AccountPage(self.page)

class AccountPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url += '/account.html'
        self.header = page.locator("div > h2")

    def navigate(self):
        super().navigate()
        expect(self.header).to_be_visible()

    @allure.step("Verify '{username}' is logged in")
    def verify_account(self, username):
        expect(self.header).to_have_text(f"Welcome, {username}!")

class GithubPRsPage(BasePage):
    def __init__(self, page,owner,repo):
        super().__init__(page)
        self.url = f"https://github.com/{owner}/{repo}/pulls"
        self.pr_name = page.locator("div[data-id] a[id*=issue]")
        self.time = page.locator("span[class=opened-by] relative-time")
        self.user = page.locator("span[class=opened-by] a")
        self.next_page_button = page.locator("a.next_page").first
        self.current_page = page.locator("a.current")
        self.new_button = page.get_by_text("New pull request")

    def navigate(self):
        super().navigate()
        expect(self.new_button).to_be_visible()

    @allure.step("Go to next page")
    def next_page(self):
        try:
            self.next_page_button.wait_for(state="visible", timeout=5000)
            if "disabled" in self.next_page_button.get_attribute("class"):
                return False
        except playwright.async_api.TimeoutError:
            return False

        currpage = int(self.current_page.inner_text())
        self.next_page_button.click()
        expect(self.current_page).to_have_text(str(currpage + 1))

        return True

    @allure.step("Scrape all the pull requests from the page")
    def get_prs(self):
        prs = []
        for i in range(self.pr_name.count()):
            row = [self.pr_name.nth(i).inner_text(), self.time.nth(i).get_attribute("datetime"), self.user.nth(i).inner_text()]
            prs.append(row)
        return prs