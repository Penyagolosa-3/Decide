from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.get("http://localhost:8000/admin/")
driver.find_element_by_id('id_username').send_keys("kwertyx")
driver.find_element_by_id('id_password').send_keys(".Asdasdasd123.",Keys.ENTER)
print('Title: %s' % driver.title)
driver.quit()
