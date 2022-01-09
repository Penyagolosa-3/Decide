
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
class TestLogin():
  
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}

  def teardown_method(self, method):
    self.driver.quit()
  
  def test_login(self):
    self.driver = webdriver.Chrome()
    self.driver.get("http://localhost:8000/booth/voting")
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) a").click()
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "username").send_keys("joura2")
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys("google123")
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    time.sleep(1)
    assert self.driver.find_element(By.CSS_SELECTOR, "h2").text == "prueba"


  def test_loginYvotar(self):
    self.driver = webdriver.Chrome()
    self.driver.get("http://localhost:8000/booth/voting")
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) a").click()
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "username").send_keys("joura2")
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys("google123")
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    time.sleep(1)
    self.driver.find_element(By.ID, "q2").click()
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    time.sleep(1)
    assert self.driver.find_element(By.ID, "q2").is_selected() is True

  def test_logout(self):
    self.driver = webdriver.Chrome()
    self.driver.get("http://localhost:8000/booth/voting")
    self.driver.set_window_size(1294, 704)
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) a").click()
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "username").send_keys("joura2")
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys("google123")
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    time.sleep(1)
    self.driver.find_element(By.LINK_TEXT, "logout").click()
    time.sleep(1)
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) a").click()
    time.sleep(1)
    assert self.driver.find_element(By.ID, "__BVID__6__BV_label_").text == "Username"