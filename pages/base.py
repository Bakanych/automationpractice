from pypom import Page
from selenium.webdriver.common.by import By


class BasePage(Page):

    def __init__(self, driver):
        super().__init__(driver)

        #TODO read from test environment settings
        self.base_url = 'http://automationpractice.com'
        self.timeout = 5

    _error_alert_loc = (By.CSS_SELECTOR, '.alert.alert-danger')

    @property
    def loaded(self):
        page_state = self.driver.execute_script('return document.readyState')
        jquery_ready = self.driver.execute_script(
            'return window.jQuery && jQuery.active == 0')
        print (type(self), page_state, jquery_ready)
        return page_state == 'complete' and jquery_ready

    # Page should not contain error alerts in valid state
    @property
    def is_valid(self):
        return not self.is_element_displayed(*self._error_alert_loc)