from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.locator('//input[@placeholder="Enter your mail"]')
        self.password_input = page.locator('//input[@placeholder="Enter your password "]')
        self.sign_in_button = page.locator('//button[@type="submit"]')

    def goto(self):
        self.page.goto("https://v2.zenclass.in/login")

    def login(self, username, password):
        self.email_input.fill(username)
        self.password_input.fill(password)
        self.sign_in_button.click()
