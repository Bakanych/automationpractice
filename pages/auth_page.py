from selenium.webdriver.common.by import By

from regions.sign_up_form import SignUpForm
from regions.sign_in_form import SignInForm
from pages.base_page import BasePage


class AuthPage(BasePage):
    URL_TEMPLATE = '/index.php?controller=authentication&back=my-account'

    _error_alert_loc = (By.CSS_SELECTOR, '.alert.alert-danger')
    _sign_up_form:SignUpForm = None
    _sign_in_form:SignInForm = None

    # Page should not contain error alerts in valid state
    #TODO: find out why sign in form displays its alerts globally on page instead of inside form
    @property
    def is_valid(self):
        return self.sign_up_form.is_valid and not self.is_element_displayed(*self._error_alert_loc)

    @property #cached form element
    def sign_up_form(self):
        if not self._sign_up_form:
            self._sign_up_form = SignUpForm(self)
        return self._sign_up_form

    @property #cached form element
    def sign_in_form(self):
        if not self._sign_in_form:
            self._sign_in_form = SignInForm(self)
        return self._sign_in_form