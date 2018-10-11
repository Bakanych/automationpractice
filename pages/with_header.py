from selenium.webdriver.common.by import By
from pages.base import BasePage


class PageWithHeader(BasePage):

    _header_loc = (By.TAG_NAME, 'h1')

    @property
    def title(self):
        return self.find_element(*self._header_loc).text

    @property
    def loaded(self):
        return super().loaded and self.is_element_displayed(*self._header_loc)

