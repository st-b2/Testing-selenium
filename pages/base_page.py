from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout, poll_frequency=0.2)

    def open(self, url):
        self.driver.get(url)
        return self

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def scroll_to(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        return element

    def click(self, locator):
        element = self.scroll_to(locator)
        try:
            self.wait.until(EC.element_to_be_clickable(locator)).click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)
        return self

    def select_by_value(self, locator, value):
        element = self.find(locator)
        Select(element).select_by_value(value)
        return self

    def type(self, locator, text):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(text)
        return self