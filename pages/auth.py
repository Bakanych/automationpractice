from pypom import Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base import BasePage
from pages.account import MyAccountPage
from pages.with_header import PageWithHeader
from pages.with_nav import PageWithNavigation
from regions.base_form import BaseForm
from regions.alert import DangerAlert, SuccessAlert


class PageWithAuth(BasePage):
    _sign_in_loc = (By.CSS_SELECTOR, 'a.login')
    _user_account_loc = (By.CSS_SELECTOR, '.header_user_info .account')
    _sign_out_loc = (By.CSS_SELECTOR, '.header_user_info .logout')

    @property
    def is_authenticated(self):
        return self.is_element_displayed(*self._user_account_loc) and \
               self.is_element_displayed(*self._sign_out_loc) and \
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
        auth_page = AuthPage(self.driver).wait_for_page_to_load()
        assert auth_page.is_valid, 'Page should not have any validation message when opened'
        return auth_page


class AuthPage(PageWithAuth, PageWithHeader, PageWithNavigation):

    URL_TEMPLATE = '/index.php?controller=authentication&back=my-account'
    _sign_up_form = None
    _sign_in_form = None


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


class ForgotPasswordPage(PageWithNavigation):

    URL_TEMPLATE = '/index.php?controller=password'
    _back_to_login_loc = (By.CSS_SELECTOR,"a[title='Back to Login']")

    @property
    def form(self):
        return ForgotPasswordForm(self)

    def back_to_login(self):
        self.find_element(*self._back_to_login_loc).click()
        self.wait_for_page_to_load()
        return AuthPage(self)



class ForgotPasswordForm(BaseForm):

    #TODO: this form has incorrect title layout. it should be inside the form. Upper element is used as root for workaround
    _root_locator = (By.ID, 'center_column')
    _email_loc = (By.ID, 'email')
    _submit_loc = (By.CSS_SELECTOR, "button[type='submit']")

    def try_retrieve_password(self, email):
        email_input = self.find_element(*self._email_loc)
        email_input.clear()
        email_input.send_keys(email)
        self.find_element(*self._submit_loc).click()

        if self.page.is_valid:
            return SuccessAlert(self.page)
        else:
            return DangerAlert(self.page)


class SignInForm(BaseForm):

    _root_locator = (By.ID, 'login_form')
    _email_loc = (By.ID, 'email')
    _password_loc = (By.ID, 'passwd')
    _submit_loc = (By.ID, 'SubmitLogin')
    _forgot_password_loc = (By.CSS_SELECTOR, '.lost_password a')

    def forgot_password(self):
        self.find_element(*self._forgot_password_loc).click()
        self.page.wait_for_page_to_load()
        return ForgotPasswordForm(self.page)
    
    def try_sign_in(self, email, password):
        email_input = self.find_element(*self._email_loc)
        email_input.clear()
        email_input.send_keys(email)
        password_input = self.find_element(*self._password_loc)
        password_input.clear()
        password_input.send_keys(password)
        self.find_element(*self._submit_loc).click()

        if self.page.is_valid:
            return MyAccountPage(self.driver).wait_for_page_to_load()
        else:
            return DangerAlert(self.page)


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


class CreateAccountForm(BaseForm):
    _root_locator = (By.ID, 'account-creation_form')

    _first_name_loc = (By.ID, 'customer_firstname')
    _last_name_loc = (By.ID, 'customer_lastname')
    _email_loc = (By.ID, 'email')
    _password_loc = (By.ID, 'passwd')
    _address_1_loc = (By.ID, 'address1')
    _city_loc = (By.ID, 'city')
    _country_loc = (By.ID, 'id_country')
    _state_loc = (By.ID, 'id_state')
    _zip_loc = (By.ID, 'postcode')
    _mobile_phone_loc = (By.ID, 'phone_mobile')

    _submit_loc = (By.ID, 'submitAccount')

    @property
    def loaded(self):
        return self.root.is_displayed()

    def register(self, account):
        self.find_element(*self._first_name_loc).send_keys(account['info']['first_name'])
        self.find_element(*self._last_name_loc).send_keys(account['info']['last_name'])
        self.find_element(*self._password_loc).send_keys(account['info']['password'])

        self.find_element(*self._address_1_loc).send_keys(account['address']['address_1'])
        self.find_element(*self._city_loc).send_keys(account['address']['city'])

        Select(self.find_element(*self._country_loc))\
            .select_by_visible_text(account['address']['country'])
        Select(self.find_element(*self._state_loc))\
            .select_by_visible_text(account['address']['state'])

        self.find_element(*self._zip_loc).send_keys(account['address']['zip'])
        self.find_element(*self._mobile_phone_loc).send_keys(account['address']['mobile_phone'])

        self.find_element(*self._submit_loc).click()

        return self.page.wait_for_page_to_load()