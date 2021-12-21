from django.test import TestCase
from voting.tests import VotingTestCase
# Create your tests here.
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

