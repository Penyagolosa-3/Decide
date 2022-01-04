

from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from base.tests import BaseTestCase
import time

class AdminTestCase(StaticLiveServerTestCase):


    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome()

        super().setUp()           

    def test_visualizer(self):
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("qwerty",Keys.ENTER)
        time.sleep(2)
        print(self.driver.current_url)
        #In case of a correct loging, a element with id 'user-tools' is shown in the upper right part
        self.assertTrue(len(self.driver.find_elements_by_id('user-tools'))==1)
        
        #Vamos a crear la votación 
        self.driver.find_element(by=By.LINK_TEXT, value="Votings").click()
        time.sleep(1)
        self.driver.find_element(by=By.XPATH, value="/html/body/div/div[3]/div/ul/li/a").click()
        self.driver.find_element_by_id('id_name').send_keys("Votacion de prueba")
        self.driver.find_element_by_id('id_desc').send_keys("Vamos a probar si funcionan los tests")
        time.sleep(1)
        #Almaceno la ventana de la votacion
        window_before = self.driver.window_handles[0]
        #Añadimos las opciones
        self.driver.find_element_by_id('add_id_question').click()
        #Almaceno la ventana de las opciones
        window_after = self.driver.window_handles[1]
        time.sleep(1)
        #Cambio de ventana
        self.driver.switch_to_window(window_after)
        self.driver.find_element_by_id('id_desc').send_keys("¿Funcionan las pruebas de decide?")
        time.sleep(1)
        self.driver.find_element_by_id('id_options-0-number').send_keys("1")
        self.driver.find_element_by_id('id_options-0-option').send_keys("Si")
        self.driver.find_element_by_id('id_options-1-number').send_keys("2")
        self.driver.find_element_by_id('id_options-1-option').send_keys("No")
        self.driver.find_element_by_id('id_options-2-number').send_keys("3")
        self.driver.find_element_by_id('id_options-2-option').send_keys("Casi")
        self.driver.find_element(by=By.XPATH, value="/html/body/div/div[1]/div/form/div/div[2]/input").click()
        time.sleep(1)    
        #Volvemos a la ventana de las votaciones
        self.driver.switch_to_window(window_before)
        window_before = self.driver.window_handles[0]
        self.driver.find_element_by_xpath('/html/body/div/div[3]/div/form/div/fieldset/div[4]/div/div[1]/a/img').click()
        window_after = self.driver.window_handles[1]
        self.driver.switch_to_window(window_after)
        self.driver.find_element_by_id('id_name').send_keys("http://localhost:8000")
        self.driver.find_element_by_id('id_url').send_keys("http://localhost:8000")
        time.sleep(1)
        self.driver.find_element_by_xpath('/html/body/div/div[1]/div/form/div/div/input').click()
        self.driver.switch_to_window(window_before)
        time.sleep(1)
        self.driver.find_element_by_xpath('/html/body/div/div[3]/div/form/div/div/input[1]').click()
        time.sleep(1)
        self.assertTrue(len(self.driver.find_elements_by_xpath('//*[@id="result_list"]/tbody/tr'))==1)
        time.sleep(2)

        #Iniciamos la votación
        self.driver.find_element_by_xpath('/html/body/div/div[3]/div/div/form/div[2]/table/tbody/tr[1]/td[1]/input').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('/html/body/div/div[3]/div/div/form/div[1]/label/select/option[3]').click()
        self.driver.find_element_by_xpath('/html/body/div/div[3]/div/div/form/div[1]/button').click()
        time.sleep(5)

        #Añadimos usuario
        self.driver.find_element_by_link_text('Home').click()
        self.driver.find_element_by_link_text('Users').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('/html/body/div/div[3]/div/ul/li/a').click()
        time.sleep(1)
        self.driver.find_element_by_id('id_username').send_keys('User1')
        self.driver.find_element_by_id('id_password1').send_keys('contraseña1')
        self.driver.find_element_by_id('id_password2').send_keys('contraseña1')
        time.sleep(1)
        self.driver.find_element_by_xpath('/html/body/div/div[3]/div/form/div/div/input[1]').click()
        time.sleep(1)
        self.driver.find_element_by_link_text('Home').click()
        self.driver.find_element_by_link_text('Users').click()
        time.sleep(3)

        self.assertTrue(len(self.driver.find_elements_by_xpath('//*[@id="result_list"]/tbody/tr'))==3)
        time.sleep(2)

        #Añadimos censo
        self.driver.find_element_by_link_text('Home').click()
        self.driver.find_element_by_link_text('Censuss').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('/html/body/div/div[3]/div/ul/li/a').click()
        time.sleep(1)
        self.driver.find_element_by_id('id_voting_id').send_keys("1")
        self.driver.find_element_by_id('id_voter_id').send_keys("2")
        self.driver.find_element_by_xpath('/html/body/div/div[3]/div/form/div/div/input[1]').click()
        time.sleep(2)
        self.assertTrue(len(self.driver.find_elements_by_xpath('//*[@id="result_list"]/tbody/tr'))==1)

        #Se realiza la votacion
        self.driver.get(f'{self.live_server_url}/booth/1/')
        self.driver.find_element_by_id('username').send_keys("admin")
        self.driver.find_element_by_id('password').send_keys("qwerty", Keys.ENTER)
        time.sleep(1)
        self.driver.find_element_by_id('q1').click()

        self.driver.find_element_by_xpath('/html/body/div/div/div/button').click()
        time.sleep(2)


    def tearDown(self):          
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()