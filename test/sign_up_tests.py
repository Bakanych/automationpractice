import json
import uuid
from pages.auth import PageWithAuth



#TODO call logout teardown fixture
def test_register_new_user_positive(browser):

    with open('account.json','r') as f:
        account = json.load(f)
    id = uuid.uuid4()
    account['info']['email'] = '{}@example.com'.format(id)

    page = PageWithAuth(browser).open()

    page.sign_in().sign_up_form\
        .try_create_account(account['info']['email'])\
        .register(account)

    assert page.is_authenticated
    assert page.header_user_info == '{} {}'.format(account['info']['first_name'], account['info']['last_name'])