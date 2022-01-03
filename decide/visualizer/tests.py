from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import sys
sys.path.insert(1, '/home/luismi/Proyectos VS/Decide/decide/')
#from base.tests import BaseTestCase
import time
import unittest

class AdminTestCase(unittest.TestCase):


    def setUp(self):
        self.driver = webdriver.Chrome() 

    def test_simpleCorrectLogin(self):                
        self.driver.get('http://www.localhost:8000/admin/')
        time.sleep(1)    
        self.driver.find_element_by_id('id_username').send_keys("luismi")
        self.driver.find_element_by_id('id_password').send_keys("contraseña1",Keys.ENTER)
        time.sleep(2) 
        print('Logueando')
        #In case of a correct loging, a element with id 'user-tools' is shown in the upper right part
        print(len(self.driver.find_elements_by_id('user-tools')))
        self.assertTrue(len(self.driver.find_elements_by_id('user-tools'))==1)       
        
    def tearDown(self):           
        self.driver.quit()



if __name__ == '__main__':
    unittest.main()


