from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods

from voting.models import Voting, QuestionOption, Question

from .models import VotingCount

from django.utils import timezone

class BoothTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

        question = Question(desc='qwerty')
        question.save()

        for i in range(5):
            self.questionOption = QuestionOption(question=question, option='option {}'.format(i+1))
            self.questionOption.save()

        self.voting = Voting(name='test voting', question=question)
        self.voting.save()

        self.votingCount = VotingCount(voting=self.voting, option=self.questionOption)
        self.votingCount.save()

    def tearDown(self):
        self.client = None

    # Descripción: Añade una nueva votación a la tabla de Recuento de votaciones
    # Entrada:
    ## option: id de la opción votada
    ## voting: id de la votación
    # Salida: ninguna
    def test_addVotingCount(self):
        # Información que se debe insertar vía POST para una opción y votación
        data = {
            'option': self.questionOption.id,
            'voting': self.voting.id
        }

        response = self.client.post('/booth/votingCount/', data, format='json')

        # Si en el endpoint se recibe id de opción válido, e id de votación, la respuesta http debería ser 200
        self.assertEqual(response.status_code, 200)

    # Descripción: Prueba la recolección de recuentos de votos en vivo a través de endpoint
    # Entrada:
    ## id: id de la votación
    # Salida: Matriz con todos los votos realizados a una votación y su opción
    def test_getVotingCount(self):
        expected_result = [
            {
                'id': self.votingCount.id,
                'voting_id': self.voting.id,
                'option_id': self.questionOption.id
            }
        ]

        # Se solicita el recuento de votos a la url añadiendo el id de la votación
        response = self.client.get('/booth/votingCount/'+str(self.voting.id)+'/', format='json')        


        # Si en el endpoint se recibe id de opción y de votación, la respuesta http debería ser 200
        self.assertEqual(response.status_code, 200)

        # Pasamos la respuesta a json y comparamos con la esperada
        values = response.json()['votingCount']
        for val in values:
            val.pop('created_at')
            
        self.assertEqual(values, expected_result)