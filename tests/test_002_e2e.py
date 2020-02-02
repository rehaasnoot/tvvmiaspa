""" this doesn't work on Safari
    remove the OFF_ to enable e2e testing
"""
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

import os
from selenium.webdriver.common.by import By
print(os.environ)
import sys
print(sys.path)

class Test_TVVMIASPA(StaticLiveServerTestCase):
    E2E = None
    def setUp(self):
        driver = webdriver.Firefox()
        self.E2E = driver

    def get_element_by_id(self, testUrl, testId):
        self.E2E.get('%s%s' % (self.live_server_url, testUrl))
        return self.E2E.find_element(by=By.ID, value=testId)

    def test_index(self):
        testUrl = "/"
        testId="tvv-app"
        testValue = "Welcome to the TVV MIA Imaginarium!?!"
        testElementValue = self.get_element_by_id(testUrl, testId).text
        self.assertEqual(testValue, testElementValue, self.__repr__())

    def test_about(self):
        testUrl = "/about"
        testId="tvv-about"
        testValue = "About TVV Musical Instrument Animator"
        self.get_element_by_id(testUrl, testId)
        self.assertIsNotNone(self.get_element_by_id(testUrl, testId), self.__repr__())

    def tearDown(self):
        self.E2E.close()
        
"""
class PythonOrgSearch(TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source
"""


