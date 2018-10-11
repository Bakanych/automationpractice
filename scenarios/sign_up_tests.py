import json
import uuid
from pages.auth import PageWithAuth


def get_account():
    with open('account.json','r') as f:
        account = json.load(f)
    id = uuid.uuid4()
    account['info']['email'] = '{}@example.com'.format(id)

    return account

def register_new_user(browser, account)->PageWithAuth:

    page = PageWithAuth(browser).open()

    page.sign_in().sign_up_form\
        .try_create_account(account['info']['email'])\
        .register(account)

    return page

#TODO call logout teardown fixture
def test_register_new_user_positive(browser):

    account = get_account()
    page = register_new_user(browser, account)

    assert page.is_authenticated
    assert page.header_user_info == '{} {}'.format(account['info']['first_name'], account['info']['last_name'])