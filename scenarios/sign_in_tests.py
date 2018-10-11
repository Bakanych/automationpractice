import pytest
import uuid
from pages.account import MyAccountPage
from regions.alert import DangerAlert, SuccessAlert
from pages.auth import AuthPage, SignInForm, ForgotPasswordPage
from scenarios.sign_up_tests import test_register_new_user_positive


@pytest.fixture(scope='module')
def auth_page(browser)->AuthPage:
    return AuthPage(browser).open()

@pytest.fixture(scope='module')
def sign_in_form(browser)->SignInForm:
    return auth_page(browser).sign_in_form

@pytest.fixture(scope='module')
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
    (('2@2.2',''), empty_password_message),
    (('2@2.2', '1'), invalid_password_message),
    (('2@2.2', '111111'), incorrect_password_message)
])
def test_sign_in_negative(sign_in_form, cred, expected_message):
    alert = sign_in_form.try_sign_in(*cred)

    assert isinstance(alert, DangerAlert)
    assert expected_message in alert.message


#TODO call logout teardown fixture
def test_sign_in_positive(sign_in_form):
    cred = ('2@2.2','qweqwe')
    alert = sign_in_form.try_sign_in(*cred)

    assert isinstance(alert, MyAccountPage)


def test_sign_in_forgot_password_link(sign_in_form):
    forgot_password_form = sign_in_form.forgot_password()

    assert 'Forgot your password?'.upper() == forgot_password_form.form_title


def test_recover_password_positive(password_page):
    existing_email = '2@2.2'
    expected_message = "A confirmation email has been sent to your address: {}".format(existing_email)
    alert = password_page.form.try_retrieve_password(existing_email)

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

    test_register_new_user_positive(browser)
    page = AuthPage(browser).open()

    assert 'My account'.upper() == page.title

