# from django.test import TestCase
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# from time import sleep
# from django.contrib.auth.models import User
# from base.tests import BaseTestCase

# class AdminTestCase(StaticLiveServerTestCase):


#   def setUp(self):
#         #Load base test functionality for decide
#         self.base = BaseTestCase()
#         self.base.setUp()

#         options = webdriver.ChromeOptions()
#         options.headless = False
#         self.driver = webdriver.Chrome(options=options)
#         self.accept_next_alert = True

#         super().setUp()

#   def tearDown(self):
#         super().tearDown()
#         self.driver.quit()

#         self.base.tearDown()
  
#   def test_exportcsv(self):
#     self.driver.get("http://127.0.0.1:8000/admin/login/?next=/admin/")
#     self.driver.set_window_size(911, 1016)
#     self.driver.find_element(By.ID, "id_username").send_keys("marmarave")
#     self.driver.find_element(By.ID, "id_password").send_keys("complexpassword")
#     self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
#     self.driver.find_element(By.LINK_TEXT, "Censuss").click()
#     self.driver.find_element(By.CSS_SELECTOR, ".export_link").click()
#     dropdown = self.driver.find_element(By.ID, "id_file_format")
#     dropdown.find_element(By.XPATH, "//option[. = 'csv']").click()
#     element = self.driver.find_element(By.ID, "id_file_format")
#     actions = ActionChains(self.driver)
#     actions.move_to_element(element).click_and_hold().perform()
#     element = self.driver.find_element(By.ID, "id_file_format")
#     actions = ActionChains(self.driver)
#     actions.move_to_element(element).perform()
#     element = self.driver.find_element(By.ID, "id_file_format")
#     actions = ActionChains(self.driver)
#     actions.move_to_element(element).release().perform()
#     self.driver.find_element(By.CSS_SELECTOR, ".default").click()
#     sleep(5)


#   def test_exportjson(self):
#     self.driver.get("http://127.0.0.1:8000/admin/login/?next=/admin/")
#     self.driver.set_window_size(911, 1016)
#     self.driver.find_element(By.ID, "id_username").send_keys("marmarave")
#     self.driver.find_element(By.ID, "id_password").send_keys("complexpassword")
#     self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
#     self.driver.find_element(By.LINK_TEXT, "Censuss").click()
#     self.driver.find_element(By.CSS_SELECTOR, ".export_link").click()
#     dropdown = self.driver.find_element(By.ID, "id_file_format")
#     dropdown.find_element(By.XPATH, "//option[. = 'json']").click()
#     element = self.driver.find_element(By.ID, "id_file_format")
#     actions = ActionChains(self.driver)
#     actions.move_to_element(element).click_and_hold().perform()
#     element = self.driver.find_element(By.ID, "id_file_format")
#     actions = ActionChains(self.driver)
#     actions.move_to_element(element).perform()
#     element = self.driver.find_element(By.ID, "id_file_format")
#     actions = ActionChains(self.driver)
#     actions.move_to_element(element).release().perform()
#     self.driver.find_element(By.CSS_SELECTOR, ".default").click()
#     sleep(5)

#   def test_export_defeat(self):
#     self.driver.get("http://127.0.0.1:8000/admin/login/?next=/admin/")
#     self.driver.set_window_size(911, 1016)
#     self.driver.find_element(By.ID, "id_username").send_keys("marmarave")
#     self.driver.find_element(By.ID, "id_password").send_keys("complexpassword")
#     self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
#     self.driver.find_element(By.LINK_TEXT, "Censuss").click()
#     self.driver.find_element(By.CSS_SELECTOR, ".export_link").click()
#     dropdown = self.driver.find_element(By.ID, "id_file_format")
#     dropdown.find_element(By.XPATH, "//option[. = '---']").click()
#     element = self.driver.find_element(By.ID, "id_file_format")
#     actions = ActionChains(self.driver)
#     actions.move_to_element(element).click_and_hold().perform()
#     element = self.driver.find_element(By.ID, "id_file_format")
#     actions = ActionChains(self.driver)
#     actions.move_to_element(element).perform()
#     element = self.driver.find_element(By.ID, "id_file_format")
#     actions = ActionChains(self.driver)
#     actions.move_to_element(element).release().perform()
#     self.driver.find_element(By.CSS_SELECTOR, ".default").click()
#     sleep(5)
  