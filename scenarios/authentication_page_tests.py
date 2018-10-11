import pytest
from pages.auth import AuthPage


@pytest.fixture(scope='module')
def auth_page(browser)->AuthPage:
    return AuthPage(browser).open()


def test_auth_page_title(auth_page):
    assert  'Authentication'.upper() == auth_page.title


def test_auth_page_contains_sign_up_form(auth_page):
    assert 'Create an account'.upper() == auth_page.sign_up_form.form_title


def test_auth_page_contains_sign_in_form(auth_page):
    assert 'Already registered?'.upper() == auth_page.sign_in_form.form_title


def test_auth_page_navigation(auth_page):
    assert auth_page.title.lower() == auth_page.current.lower()
    assert 1 == len(auth_page.nav_items)
    assert  'Return to Home' == auth_page.nav_items[0]

def test_sign_in_form_is_valid(auth_page):
    form = auth_page.sign_in_form
    assert True == form.is_field_valid('Email address')
    assert True == form.is_field_valid('Password')

def test_sign_up_form_is_valid(auth_page):
    form = auth_page.sign_up_form
    assert True == form.is_valid
    assert True == form.is_field_valid('Email address')

