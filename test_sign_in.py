import pytest

from pages.my_account_page import MyAccountPage
from regions.sign_in_form import SignInForm
from regions.danger_alert import DangerAlert
from pages.auth_page import AuthPage


@pytest.fixture(scope='module')
def auth_page(browser)->AuthPage:
    return AuthPage(browser).open()

@pytest.fixture(scope='module')
def sign_in_form(browser)->SignInForm:
    return auth_page(browser).sign_in_form

"""
@Negative
Check form validation trying to sign in with empty or invalid email
"""

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


def test_sign_in_positive(sign_in_form):
    cred = ('2@2.2','11111')
    alert = sign_in_form.try_sign_in(*cred)
    assert isinstance(alert, MyAccountPage)