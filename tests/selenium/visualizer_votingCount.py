from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time

options = webdriver.ChromeOptions()
options.headless = True

visualizer = webdriver.Chrome()

visualizer.get("http://localhost:8000/visualizer/2/")
print(visualizer.find_element(by=By.XPATH, value="//div[@id='app-visualizer']/div/div/table/tbody/tr[3]/td[2]").text)

voter = webdriver.Chrome()
voter.get("http://localhost:8000/booth/2/")
voter.find_element_by_id("username").clear()
voter.find_element_by_id("username").send_keys("testito")
voter.find_element_by_id("password").clear()
voter.find_element_by_id("password").send_keys(".Asdasdasd123.")
voter.find_element_by_xpath("//button[@type='submit']").click()
time.sleep(2)

firstVal = visualizer.find_element(by=By.XPATH, value="//div[@id='app-visualizer']/div/div/table/tbody/tr/td[2]").text
print("Votación sin actualizar de la primera opcion: "+firstVal)

voter.find_element_by_id("q1").click()
voter.find_element_by_xpath("//button[@type='button']").click()
print("Votación realizada")
voter.quit()
time.sleep(2)

secondVal = visualizer.find_element(by=By.XPATH, value="//div[@id='app-visualizer']/div/div/table/tbody/tr/td[2]").text
print("Votación actualizada de la primera opcion: "+secondVal)

print(int(firstVal)+1 == int(secondVal))

time.sleep(20)

visualizer.quit()
