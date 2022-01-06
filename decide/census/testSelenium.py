from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.get("http://127.0.0.1:8000/admin/")
driver.find_element_by_id('id_username').send_keys("decide")
driver.find_element_by_id('id_password').send_keys("decide",Keys.ENTER)
driver.get("http://127.0.0.1:8000/admin/census/census/")
driver.find_element(By.CSS_SELECTOR, ".export_link").click()
driver.find_element_by_id('id_file_format').send_keys(Keys.DOWN)
driver.find_element(By.CSS_SELECTOR, ".default").click()
sleep(10)
print('Title: %s' % driver.title)
driver.quit()