from playwright.sync_api import Page

class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
        self.profile_icon = page.locator('//div[contains(@class, "profile-click-icon-div")]')
        self.logout_button = page.locator("//div[contains(@class,'user-avatar-menu') and text()='Log out']")

    def logout(self):
        # Ensure any backdrop disappears before clicking
        backdrop = self.page.locator('.MuiBackdrop-root')
        if backdrop.is_visible():
            backdrop.wait_for(state="hidden", timeout=5000)
        self.profile_icon.click()
        self.logout_button.click()
