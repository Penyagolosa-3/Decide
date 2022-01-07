from voting.tests import VotingTestCase
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from voting.models import Voting, QuestionOption, Question

from census.models import Census

from booth.models import VotingCount

from django.utils import timezone

from base.tests import BaseTestCase
import time

from django.contrib.auth.models import User
from mixnet.models import Auth

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
        self.driver.get(self.live_server_url+'/admin/')
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
        #self.driver.get(self.live_server_url+'/booth/1/')
        #self.driver.find_element_by_id('username').send_keys("admin")
        #self.driver.find_element_by_id('password').send_keys("qwerty", Keys.ENTER)
        #time.sleep(1)
        #self.driver.find_element_by_id('q1').click()

        #self.driver.find_element_by_xpath('/html/body/div/div/div/button').click()
        #time.sleep(2)


    def tearDown(self):          
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()


class VisualizerTestCase(VotingTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def voteTallied(self):
        voting = self.create_voting()
        self.login()
        for action in ['start','stop', 'tally']:
            data = {'action': action}
            response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        return voting.pk

    def test_recibir_votos(self):
        votingpk = self.voteTallied()

        data = {'update_id': 339892899, 'message': {'message_id': 285, 'from': {'id': 2004953283, 'is_bot': False, 'first_name': 'Lui', 'language_code': 'es'}, 'chat': {'id': 0, 'first_name': 'Lui', 'type': 'private'}, 'date': 1640018166, 'text': '/start', 'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}}
        response = self.client.put('/webhooks', data, format='json')
        self.assertEqual(response.status_code, 301)
        data2 = {'update_id': 339892900, 'message': {'message_id': 287, 'from': {'id': 2004953283, 'is_bot': False, 'first_name': 'Lui', 'language_code': 'es'}, 'chat': {'id': 0, 'first_name': 'Lui', 'type': 'private'}, 'date': 1640018174, 'text': '/visualizer {}'.format(votingpk), 'entities': [{'offset': 0, 'length': 11, 'type': 'bot_command'}]}}
        response = self.client.post('/webhooks', data2, format='json')
        self.assertEqual(response.status_code, 301)


class LiveVotingCountTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()

        self.voter = User(username='testitoValiente')
        self.voter.set_password('qwerty')
        self.voter.is_active = True
        self.voter.save()

        self.voting = self.create_voting()

        c = Census(voter_id=self.voter.id, voting_id=self.voting.id)
        c.save()

        options = webdriver.ChromeOptions()
        options.headless = True

        super().setUp()

    def tearDown(self):          
        super().tearDown()

        self.base.tearDown()

    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=self.live_server_url,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        return v

    def test_showLiveVotingCount(self):
        visualizer = webdriver.Chrome()

        visualizer.get(self.live_server_url+'/visualizer/'+str(self.voting.id)+'/')

        voter = webdriver.Chrome()
        voter.get(self.live_server_url+'/booth/'+str(self.voting.id)+'/')
        voter.find_element_by_id("username").clear()
        voter.find_element_by_id("username").send_keys(self.voter.username)
        voter.find_element_by_id("password").clear()
        voter.find_element_by_id("password").send_keys("qwerty")
        voter.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(2)

        firstVal = visualizer.find_element(by=By.XPATH, value="//div[@id='app-visualizer']/div/div/table/tbody/tr/td[2]").text

        voter.find_element_by_id("q1").click()
        voter.find_element_by_xpath("//button[@type='button']").click()
        time.sleep(2)

        secondVal = visualizer.find_element(by=By.XPATH, value="//div[@id='app-visualizer']/div/div/table/tbody/tr/td[2]").text

        visualizer.quit()
        voter.quit()

        self.assertEqual(int(firstVal)+1, int(secondVal))
        