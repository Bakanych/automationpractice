import json
import uuid

import pytest

from pages.base import BasePage


#TODO call logout teardown fixture
@pytest.fixture(scope='module')
def page(browser)->BasePage:
    return BasePage(browser).open()

def test_register_new_user_positive(page):
    with open('account.json','r') as f:
        account = json.load(f)
    id = uuid.uuid4()
    account['info']['email'] = '{}@example.com'.format(id)

    page.sign_in().sign_up_form\
        .try_create_account(account['info']['email'])\
        .register(account)

    assert page.is_authenticated
    assert page.header_user_info == '{} {}'.format(account['info']['first_name'], account['info']['last_name'])