import pytest

from page_regions import SignUpForm, DangerAlert
from pages import AuthPage

@pytest.fixture(scope='module')
def auth_page(browser)->AuthPage:
    return AuthPage(browser).open()

@pytest.fixture(scope='module')
def sign_up_form(browser)->SignUpForm:
    return AuthPage(browser).open().sign_up_form


def test_page_contains_create_account_form(auth_page):
    assert auth_page.sign_up_form.title == 'Create an account'.upper()


def test_page_contains_already_registered_form(auth_page):
    assert auth_page.sign_in_form.title == 'Already registered?'.upper()


invalid_email_expected_message = 'Invalid email address.'
@pytest.mark.parametrize('email,expected_message', [
    ('',invalid_email_expected_message),
    ('a', invalid_email_expected_message),
    ('a@', invalid_email_expected_message),
    ('a@a', invalid_email_expected_message),
    ('a@a.', invalid_email_expected_message)
])
def test_sign_up_should_validate_empty_email(sign_up_form, email, expected_message):
    result_page = sign_up_form.try_create_account(email)
    assert isinstance(result_page, DangerAlert)
    assert result_page.message == invalid_email_expected_message

def test(sign_up_form):
    result_page = sign_up_form.try_create_account()
    assert isinstance(result_page, DangerAlert)

