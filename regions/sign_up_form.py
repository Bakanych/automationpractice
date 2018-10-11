from selenium.webdriver.common.by import By

from regions.base_form import BaseForm
from regions.create_account_form import CreateAccountForm
from regions.danger_alert import DangerAlert


class SignUpForm(BaseForm):
    _root_locator = (By.ID, 'create-account_form')
    _email_loc = (By.ID, 'email_create')
    _submit_loc = (By.ID, 'SubmitCreate')
    _error_alert_loc = (By.CSS_SELECTOR, '.alert.alert-danger')

    @property
    def is_valid(self):
        self.page.wait_for_page_to_load()
        return not self.is_element_displayed(*self._error_alert_loc)

    def try_create_account(self, email=''):
        email_input = self.find_element(*self._email_loc)
        email_input.clear()
        email_input.send_keys(email)
        self.find_element(*self._submit_loc).click()

        if self.is_valid:
            return CreateAccountForm(self.page)
        else:
            return DangerAlert(self)