from pypom import Region
from selenium.webdriver.common.by import By

#TODO refactor to universal alert

class DangerAlert(Region):
    _root_locator = (By.CSS_SELECTOR, '.alert.alert-danger')

    @property
    def loaded(self):
        return self.root.is_displayed()

    @property
    def message(self):
        return self.root.text


class SuccessAlert(Region):
    _root_locator = (By.CSS_SELECTOR, '.alert.alert-success')

    @property
    def loaded(self):
        return self.root.is_displayed()

    @property
    def message(self):
        return self.root.text