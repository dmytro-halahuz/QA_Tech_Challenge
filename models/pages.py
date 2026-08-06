import allure
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