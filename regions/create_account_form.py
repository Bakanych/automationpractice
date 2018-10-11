from pypom import Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class CreateAccountForm(Region):
    _root_locator = (By.ID, 'account-creation_form')

    _first_name_loc = (By.ID, 'customer_firstname')
    _last_name_loc = (By.ID, 'customer_lastname')
    _email_loc = (By.ID, 'email')
    _password_loc = (By.ID, 'passwd')
    _address_1_loc = (By.ID, 'address1')
    _city_loc = (By.ID, 'city')
    _country_loc = (By.ID, 'id_country')
    _state_loc = (By.ID, 'id_state')
    _zip_loc = (By.ID, 'postcode')
    _mobile_phone_loc = (By.ID, 'phone_mobile')

    _submit_loc = (By.ID, 'submitAccount')

    @property
    def loaded(self):
        return self.root.is_displayed()

    def register(self, account):
        self.find_element(*self._first_name_loc).send_keys(account['info']['first_name'])
        self.find_element(*self._last_name_loc).send_keys(account['info']['last_name'])
        self.find_element(*self._password_loc).send_keys(account['info']['password'])

        self.find_element(*self._address_1_loc).send_keys(account['address']['address_1'])
        self.find_element(*self._city_loc).send_keys(account['address']['city'])

        Select(self.find_element(*self._country_loc))\
            .select_by_visible_text(account['address']['country'])
        Select(self.find_element(*self._state_loc))\
            .select_by_visible_text(account['address']['state'])

        self.find_element(*self._zip_loc).send_keys(account['address']['zip'])
        self.find_element(*self._mobile_phone_loc).send_keys(account['address']['mobile_phone'])

        self.find_element(*self._submit_loc).click()

        return self.page.wait_for_page_to_load()