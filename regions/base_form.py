from pypom import Region
from selenium.webdriver.common.by import By


class BaseForm(Region):
    _header_loc = (By.CSS_SELECTOR,'h3.page-subheading')

    @property
    def title(self):
        return self.find_element(*self._header_loc).text