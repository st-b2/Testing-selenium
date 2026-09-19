import pytest
from utils.browsers import create_driver

@pytest.fixture
def driver():
    drv = create_driver("chrome", headless=False)
    yield drv
    drv.quit()