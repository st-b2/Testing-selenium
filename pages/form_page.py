from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class FormPage(BasePage):
    URL = "https://practice-automation.com/form-fields/"

    NAME = (By.ID, "name-input")
    EMAIL = (By.ID, "email")
    PASSWORD = (By.CSS_SELECTOR, "input[type='password']")
    MESSAGE = (By.CSS_SELECTOR, "textarea[name='message']")
    AUTOMATION = (By.ID, "automation")
    SUBMIT = (By.ID, "submit-btn")

    def load(self):
        return self.open(self.URL)

    def fill(self, data):
        self.type(self.NAME, data["name"])
        self.type(self.PASSWORD, data["password"])

        for drink in data["drinks"]:
            locator = (By.CSS_SELECTOR, f"input[name='drink'][value='{drink}']")
            element = self.find(locator)
            if not element.is_selected():
                element.click()

        self.click((By.CSS_SELECTOR, f"input[name='fav_color'][value='{data['color']}']"))

        self.select_by_value(self.AUTOMATION, data["automation"])

        self.type(self.EMAIL, data["email"])
        self.type(self.MESSAGE, data["message"])
        return self

    def submit_n_read_alert(self):
        self.click(self.SUBMIT)
        self.wait.until(lambda d: d.switch_to.alert)
        alert = self.driver.switch_to.alert
        text = alert.text
        alert.accept()
        return text
