import pytest
from regions.sign_up_form import SignUpForm
from regions.danger_alert import DangerAlert
from pages.auth_page import AuthPage


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
    ('@', invalid_email_expected_message),
    ('a', invalid_email_expected_message),
    ('a@', invalid_email_expected_message),
    ('a@a', invalid_email_expected_message),
    ('a@a.', invalid_email_expected_message)
])
def test_sign_up_validate_invalid_email(sign_up_form, email, expected_message):
    result_page = sign_up_form.try_create_account(email)
    assert isinstance(result_page, DangerAlert)
    assert result_page.message == invalid_email_expected_message


existing_email_expected_message = 'An account using this email address has already been registered. ' \
                                  'Please enter a valid password or request a new one.'
def test_sign_up_validate_existing_email(sign_up_form):
    #TODO create and use new account email as arrange step
    existing_email = '1@1.1'
    result_page = sign_up_form.try_create_account(existing_email)
    assert isinstance(result_page, DangerAlert)
    assert result_page.message == existing_email_expected_message


