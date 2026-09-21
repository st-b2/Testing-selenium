from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def create_driver(browser: str = "chrome", headless: bool = False):
    if browser.lower() == "chrome":
        opts = ChromeOptions()
        if headless:
            opts.add_argument("--headless=new")
        return webdriver.Chrome(options=opts)

    elif browser == "firefox":
        opts = FirefoxOptions()
        if headless:
            opts.add_argument("-headless")
        return webdriver.Firefox(options=opts)

    raise ValueError(f"Неизвестный браузер: {browser}")