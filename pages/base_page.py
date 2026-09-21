from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)
        return self

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def select_by_value(self, locator, value):
        element = self.find(locator)
        Select(element).select_by_value(value)
        return self

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        return self

    def type(self, locator, text):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(text)
        return self