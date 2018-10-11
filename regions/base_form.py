from typing import Dict

from pypom import Region
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class BaseForm(Region):
    _header_loc = (By.CSS_SELECTOR,'h3.page-subheading')

    def _field_input_loc(self, label):
        return (By.XPATH, ".//div[./label='{}']".format(label))

    def is_field_valid(self, label):
        group_elem:WebElement = self.find_element(*self._field_input_loc(label))
        return not 'form-error' in group_elem.get_attribute('class')

    @property
    def form_title(self):
        return self.find_element(*self._header_loc).text