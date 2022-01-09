from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.keys import Keys


from base.tests import BaseTestCase

class AdminTestCase(StaticLiveServerTestCase):


    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        self.accept_next_alert = True

        self.githubEmail = 'jquitzonp_j492r@vixej.com'
        super().setUp()            
            
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def test_loginAdminSuccess(self):
        driver = self.driver
        driver.get("http://localhost:8000/admin")
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("jesus")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("practica",Keys.ENTER)
        self.assertEqual("Django administration", driver.find_element_by_link_text("Django administration").text)
        driver.get("http://localhost:8000/admin/logout")
    
    def test_loginAuthGithubSuccess(self):
        driver = self.driver
        driver.get("http://localhost:8000/authentication/accounts/github/login/")
        driver.find_element_by_id("login_field").clear()
        driver.find_element_by_id("login_field").send_keys("penyagolosa-1-decide")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("Jornada2022")
        driver.find_element_by_id("password").send_keys(Keys.ENTER)
        WebDriverWait(driver, 15)
        self.assertEqual(driver.current_url, "http://localhost:8000/booth/voting" )

    def test_loginAuthGithubError(self):
        driver = self.driver
        driver.get("http://localhost:8000/authentication/accounts/github/login/")
        driver.find_element_by_id("login_field").clear()
        driver.find_element_by_id("login_field").send_keys("penyagolosa-1-decide")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("123")
        driver.find_element_by_name("commit").click()
        self.assertEqual("Incorrect username or password.", driver.find_element_by_xpath("//div[@id='js-flash-container']/div/div").text)


