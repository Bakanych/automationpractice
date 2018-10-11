import pytest
import uuid
from regions.alert import DangerAlert, SuccessAlert
from pages.auth import AuthPage, SignInForm, ForgotPasswordPage, MyAccountPage
from scenarios.sign_up_tests import get_account, register_new_user

existing_account_email = '2@2.2'
existing_account_password = 'qweqwe'

@pytest.fixture()
def auth_page(browser)->AuthPage:
    return AuthPage(browser).open()

@pytest.fixture()
def sign_in_form(browser)->SignInForm:
    return auth_page(browser).sign_in_form

@pytest.fixture()
def password_page(browser)->ForgotPasswordPage:
    return ForgotPasswordPage(browser).open()


invalid_email_message = 'Invalid email address.'
invalid_password_message = 'Invalid password.'
incorrect_password_message = 'Authentication failed.'
empty_email_message = 'An email address required.'
empty_password_message = 'Password is required.'

@pytest.mark.parametrize('cred,expected_message', [
    (('',''),empty_email_message),
    (('@',''), invalid_email_message),
    (('a',''), invalid_email_message),
    (('a@',''), invalid_email_message),
    (('a@a',''), invalid_email_message),
    (('a@a.',''), invalid_email_message),
    ((existing_account_email,''), empty_password_message),
    ((existing_account_email, '1'), invalid_password_message),
    ((existing_account_email, '111111'), incorrect_password_message)
])
def test_sign_in_negative(sign_in_form, cred, expected_message):
    alert = sign_in_form.try_sign_in(*cred)

    assert isinstance(alert, DangerAlert)
    assert expected_message in alert.message


def test_sign_in_positive(sign_in_form):
    cred = (existing_account_email,existing_account_password)
    account_page = sign_in_form.try_sign_in(*cred)

    assert isinstance(account_page, MyAccountPage)

    account_page.sign_out()


def test_forgot_password_link(sign_in_form):
    forgot_password_form = sign_in_form.forgot_password()

    assert 'Forgot your password?'.upper() == forgot_password_form.form_title


def test_recover_password_positive(password_page):
    expected_message = "A confirmation email has been sent to your address: {}".format(existing_account_email)
    alert = password_page.form.try_retrieve_password(existing_account_email)

    assert isinstance(alert, SuccessAlert)
    assert expected_message == alert.message


@pytest.mark.parametrize('email,expected_message', [
    ('',invalid_email_message),
    ('123', invalid_email_message),
    ('{}@example.com'.format(uuid.uuid4()), 'There is no account registered for this email address.')
])
def test_recover_password_negative(password_page, email, expected_message):
    alert = password_page.form.try_retrieve_password(email)

    assert isinstance(alert, DangerAlert)
    assert expected_message in alert.message

def test_recover_password_navigate_back_button(password_page):
    assert isinstance(password_page.back_to_login(), AuthPage)

def test_recover_password_navigate_back_breadcrumb(password_page):
    index = password_page.nav_items.index('Authentication')
    password_page.navigate(index)
    expected_page = AuthPage(password_page.driver)
    assert 'Authentication'.upper() == expected_page.title

def test_logged_user_cannot_login_using_direct_link(browser):

    register_new_user(browser, get_account())
    page = AuthPage(browser).open()

    assert 'My account'.upper() == page.title

