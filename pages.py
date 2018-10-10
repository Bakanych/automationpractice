from pypom import Page
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from page_regions import SignUpForm, SignInForm


class BasePage(Page):

    def __init__(self, driver):
        super().__init__(driver)

        #TODO read from test environment settings
        self.base_url = 'http://automationpractice.com'
        self.timeout = 5

    _sign_in_loc = (By.CSS_SELECTOR, 'a.login')
    _user_account_loc = (By.CSS_SELECTOR, '.header_user_info .account')
    _sign_out_loc = (By.CSS_SELECTOR,'.header_user_info .logout')

    @property
    def loaded(self):
        page_state = self.driver.execute_script('return document.readyState')
        jquery_ready = self.driver.execute_script(
            'return window.jQuery && jQuery.active == 0')
        #print (page_state, jquery_ready)
        return page_state == 'complete' and jquery_ready

    @property
    def is_authenticated(self):
        return  self.is_element_displayed(*self._user_account_loc) and\
                self.is_element_displayed(*self._sign_out_loc) and\
                not self.is_element_present(*self._sign_in_loc)

    @property
    def header_user_info(self):
        return self.find_element(*self._user_account_loc).text

    def sign_out(self):
        assert self.is_authenticated, 'Cannot sign out: User is not signed in'
        self.find_element(*self._sign_out_loc).click()
        assert not self.is_authenticated
        return self

    def sign_in(self):
        assert not self.is_authenticated, 'Cannot sign in: User already signed in'
        self.find_element(*self._sign_in_loc).click()
        auth_page = AuthPage(self.driver)
        assert auth_page.is_valid, 'Authentication page should not have any validation message when opened'
        return auth_page


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



