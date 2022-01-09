
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
class TestPrueba():

  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  def teardown_method(self, method):
    self.driver.quit()
  def test_ventanaDeLogeo(self):
    self.driver = webdriver.Chrome()
    self.driver.get("http://localhost:8000/booth/voting")
    self.driver.set_window_size(1050, 518)
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) a").click()
    self.driver.find_element(By.XPATH, "//div[@id=\'customBtn\']/a/span").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "#headingText > span").text == "Iniciar sesión"
  def test_cuentaNoExistente(self):
    self.driver = webdriver.Chrome()
    self.driver.get("http://localhost:8000/booth/voting")
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) a").click()
    self.driver.find_element(By.XPATH, "//div[@id=\'customBtn\']/a/span").click()
    self.driver.find_element(By.ID, "identifierId").send_keys("jouradecide")
    self.driver.find_element(By.CSS_SELECTOR, ".VfPpkd-LgbsSe-OWXEXe-k8QpJ > .VfPpkd-vQzf8d").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".VfPpkd-LgbsSe-OWXEXe-k8QpJ > .VfPpkd-vQzf8d")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    assert self.driver.find_element(By.CSS_SELECTOR, ".o6cuMc").text == "No se ha podido encontrar tu cuenta de Google"
  def test_usuariosiexiste(self):
    self.driver = webdriver.Chrome()
    self.driver.get("http://localhost:8000/booth/voting")
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) a").click()
    self.driver.find_element(By.XPATH, "//div[@id=\'customBtn\']/a/span").click()
    self.driver.find_element(By.ID, "identifierId").send_keys("innosoft2021.16")
    self.driver.find_element(By.CSS_SELECTOR, ".VfPpkd-LgbsSe-OWXEXe-k8QpJ > .VfPpkd-vQzf8d").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".VfPpkd-LgbsSe-OWXEXe-k8QpJ > .VfPpkd-vQzf8d")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    assert self.driver.find_element(By.CSS_SELECTOR, ".kHn9Lb").text == "Iniciar sesión con Google"
  