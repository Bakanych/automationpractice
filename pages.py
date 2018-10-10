from pypom import Page
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from page_regions import SignUpForm, SignInForm


class BasePage(Page):

    def __init__(self, driver):
        super().__init__(driver)
        self.base_url = 'http://automationpractice.com'

    _sign_in_loc = (By.CSS_SELECTOR, 'a.login')
    _user_account_loc = (By.CSS_SELECTOR, '.header_user_info .account')
    _sign_out_loc = (By.CSS_SELECTOR,'.header_user_info .logout')

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
        return AuthPage(self.driver)


class AuthPage(BasePage):
    URL_TEMPLATE = '/index.php?controller=authentication&back=my-account'

    @property
    def sign_up_form(self):
        return SignUpForm(self)

    @property
    def sign_in_form(self):
        return SignInForm(self)



