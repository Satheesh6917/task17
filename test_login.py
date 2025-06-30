import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.home_page import DashboardPage
import pytest

valid_username = "satheeshkanna441@gmail.com"
valid_password = "Bakunamatata@123"
invalid_username = "invalid_user@test.com"
invalid_password = "invalid_pass"

@pytest.fixture(scope="function")
def setup_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()

def test_successful_login_and_logout(setup_browser):
    page = setup_browser
    login = LoginPage(page)
    dashboard = DashboardPage(page)
    
    login.goto()
    login.login(valid_username, valid_password)
    
    page.wait_for_url("**/dashboard*", timeout=10000)
    assert "dashboard" in page.url.lower(), f"Login might have failed, current URL: {page.url}"
    
    dashboard.logout()
    page.wait_for_url("**/login*", timeout=10000)
    assert "login" in page.url.lower(), f"Logout might have failed, current URL: {page.url}"

def test_unsuccessful_login(setup_browser):
    page = setup_browser
    login = LoginPage(page)
    
    login.goto()
    login.login(invalid_username, invalid_password)
    
    page.wait_for_timeout(3000)
    assert "login" in page.url.lower(), "Expected to remain on login page with invalid credentials"

def test_validate_input_boxes(setup_browser):
    page = setup_browser
    login = LoginPage(page)
    
    login.goto()
    
    assert login.email_input.is_visible(), "Username input box is not visible"
    assert login.email_input.is_enabled(), "Username input box is not enabled"
    assert login.password_input.is_visible(), "Password input box is not visible"
    assert login.password_input.is_enabled(), "Password input box is not enabled"

def test_validate_submit_button(setup_browser):
    page = setup_browser
    login = LoginPage(page)
    
    login.goto()
    
    assert login.sign_in_button.is_visible(), "Submit button is not visible"
    assert login.sign_in_button.is_enabled(), "Submit button is not enabled"
    
    login.sign_in_button.click()
    
    page.wait_for_timeout(3000)
    assert "login" in page.url.lower(), "Should remain on login page when credentials are empty"

def test_logout_button_functionality(setup_browser):
    page = setup_browser
    login = LoginPage(page)
    dashboard = DashboardPage(page)
    
    login.goto()
    login.login(valid_username, valid_password)
    page.wait_for_url("**/dashboard*", timeout=10000)
    assert "dashboard" in page.url.lower(), "Login failed, dashboard not reached"
    
    dashboard.logout()
    page.wait_for_url("**/login*", timeout=10000)
    assert "login" in page.url.lower(), "Logout did not redirect to login page"