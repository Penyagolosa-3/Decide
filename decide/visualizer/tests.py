from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from voting.models import Voting, QuestionOption, Question

from census.models import Census

from django.utils import timezone

from base.tests import BaseTestCase
import time

from django.contrib.auth.models import User
from mixnet.models import Auth

from booth.models import VotingCount

class LiveVotingCountTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()

        self.voter = User(username='testitoValiente')
        self.voter.set_password('qwerty')
        self.voter.is_active = True
        self.voter.save()

        options = webdriver.ChromeOptions()
        options.headless = True

        super().setUp()

    def scena(self):
        voting = self.create_voting()

        c = Census(voter_id=self.voter.id, voting_id=voting.id)
        c.save()

        return voting

    def tearDown(self):          
        super().tearDown()

        self.base.tearDown()

    def create_voting(self):
        q = Question.objects.get_or_create(desc='test question')
        
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=self.live_server_url, defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)
        v.save()

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        return v

    def test_registerVoteCount(self):
        voting = self.scena()

        votingCount = VotingCount.objects.filter(voting_id=voting.id)
        first = len(votingCount)

        voter = webdriver.Chrome()
        voter.get(self.live_server_url+'/booth/'+str(voting.id)+'/')
        voter.find_element_by_id("username").clear()
        voter.find_element_by_id("username").send_keys(self.voter.username)
        voter.find_element_by_id("password").clear()
        voter.find_element_by_id("password").send_keys("qwerty")
        voter.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(2)

        voter.find_element(by=By.XPATH, value="/html/body/div/div/div/fieldset[1]/div/div/input").click()
        voter.find_element_by_xpath("//button[@type='button']").click()
        time.sleep(1)
        voter.quit()
        time.sleep(2)

        votingCount = VotingCount.objects.filter(voting_id=voting.id)
        after = len(votingCount)

        self.assertEqual(first+1, after)

    def test_showLiveVotingCount(self):

        voting = self.scena()

        visualizer = webdriver.Chrome()

        visualizer.get(self.live_server_url+'/visualizer/'+str(voting.id)+'/')

        voter = webdriver.Chrome()
        voter.get(self.live_server_url+'/booth/'+str(voting.id)+'/')
        voter.find_element_by_id("username").clear()
        voter.find_element_by_id("username").send_keys(self.voter.username)
        voter.find_element_by_id("password").clear()
        voter.find_element_by_id("password").send_keys("qwerty")
        voter.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(2)

        firstVal = visualizer.find_element(by=By.XPATH, value="//div[@id='app-visualizer']/div/div/table/tbody/tr/td[2]").text

        voter.find_element(by=By.XPATH, value="/html/body/div/div/div/fieldset[1]/div/div/input").click()
        voter.find_element_by_xpath("//button[@type='button']").click()
        time.sleep(1)
        voter.quit()
        time.sleep(2)

        secondVal = visualizer.find_element(by=By.XPATH, value="//div[@id='app-visualizer']/div/div/table/tbody/tr/td[2]").text

        visualizer.quit()

        self.assertEqual(int(firstVal)+1, int(secondVal))
        