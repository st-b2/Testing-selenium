import pytest
from utils.browsers import create_driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="chrome | firefox | edge")
    parser.addoption("--headless", action="store_true",
                     help="Запуск без окна")
    parser.addoption("--grid-url", action="store", default=None,
                     help="URL Selenium Grid (например http://localhost:4444)")


@pytest.fixture
def driver(request):
    grid_url = request.config.getoption("--grid-url")
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    if grid_url:
        # УДАЛЁННЫЙ режим: подключаемся к Chrome в контейнере
        opts = Options()
        if headless:
            opts.add_argument("--headless=new")
        drv = webdriver.Remote(command_executor=grid_url, options=opts)
    else:
        # ЛОКАЛЬНЫЙ режим
        drv = create_driver(browser=browser, headless=headless)

    drv.implicitly_wait(5)
    yield drv
    drv.quit()