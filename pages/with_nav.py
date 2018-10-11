from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.base import BasePage


class PageWithNavigation(BasePage):

    _nav_loc = (By.CSS_SELECTOR, '.breadcrumb')
    _current_page_loc = (By.CSS_SELECTOR, '.breadcrumb span.navigation_page')
    _navigation_links_loc = (By.CSS_SELECTOR, '.breadcrumb a[title]')

    @property
    def _nav_elements(self):
        return self.find_elements(*self._navigation_links_loc)

    @property
    def current(self):
        return self.find_element(*self._current_page_loc).text

    @property
    def nav_items(self):
        return [el.get_attribute('title') for el in self._nav_elements]

    def navigate(self, index):
        self._nav_elements[index].click()





