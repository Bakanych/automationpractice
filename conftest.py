from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import pytest


@property
def base_url():
    return 'qwe'

@pytest.fixture(scope="session")
def browser():
    opts = Options()
    opts.headless = False
    browser = Chrome(options=opts)
    browser.maximize_window()
    return browser


#TODO close browser if error occured
@pytest.fixture(scope="session")
def browser_fixture(browser):
    yield
    browser.close()
