""" this doesn't work on Safari
    remove the OFF_ to enable e2e testing
"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        from apps.settings import SECRETS_JSON
        testLogin = SECRETS_JSON.get('e2etestlogin')
        testPasswd = SECRETS_JSON.get('e2etestpassword')
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(testLogin)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(testPasswd)
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()