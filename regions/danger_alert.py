from pypom import Region
from selenium.webdriver.common.by import By


class DangerAlert(Region):
    _root_locator = (By.CSS_SELECTOR, '.alert.alert-danger')

    @property
    def loaded(self):
        return self.root.is_displayed()

    @property
    def message(self):
        return self.root.text