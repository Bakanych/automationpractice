import pytest
from pages import AuthPage

@pytest.fixture(scope='module')
def auth_page(browser)->AuthPage:
    return AuthPage(browser).open()

def test_page_contains_create_account_form(auth_page:AuthPage):
    assert auth_page.sign_up_form.title == 'Create an account'.upper()

def test_page_contains_already_registered_form(auth_page:AuthPage):
    assert auth_page.sign_in_form.title == 'Already registered?'.upper()
