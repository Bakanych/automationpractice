from selenium.webdriver.common.by import By

from regions.base_form import BaseForm
from pages.my_account_page import MyAccountPage
from regions.danger_alert import DangerAlert


class SignInForm(BaseForm):
    _root_locator = (By.ID, 'login_form')

    _email_loc = (By.ID, 'email')
    _password_loc = (By.ID, 'passwd')
    _submit_loc = (By.ID, 'SubmitLogin')

    def try_sign_in(self, email, password):
        email_input = self.find_element(*self._email_loc)
        email_input.clear()
        email_input.send_keys(email)
        password_input = self.find_element(*self._password_loc)
        password_input.clear()
        password_input.send_keys(password)
        self.find_element(*self._submit_loc).click()

        if self.page.is_valid:
            return MyAccountPage(self.driver)
        else:
            return DangerAlert(self.page)