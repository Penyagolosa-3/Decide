from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    def test_identity(self):
        data = {
            'type': 'IDENTITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_borda(self):
        """
            * Definición: Test que verifica que el algoritmo borda funciona correctamente
            * Entrada: Votación
                - Number: id de la opción
                - Option: nombre de la opción
                - Votes: Número de votos que recibe en la votación
                - Group: Grupo de votación al que pertenece
            * Salida: los datos de entrada con un nuevo parámetro llamado total
            que supone el valor de esa opción tras aplicar el algoritmo
        """        
        data = {
            "type": "BORDA",	
            "options": [
                { "option": "Option 1", "number": 1, "votes": 3, "group":"g1" },
                { "option": "Option 2", "number": 2, "votes": 26, "group":"g1" },
                { "option": "Option 3", "number": 3, "votes": 9, "group":"g1" },
                { "option": "Option 1", "number": 4, "votes": 12, "group":"g2" },
                { "option": "Option 2", "number": 5, "votes": 7, "group":"g2" },
                { "option": "Option 3", "number": 6, "votes": 2, "group":"g2" }
            ]
        }
        expected_result = [
                { "option": "Option 2", "number": 2, "votes": 26, "group":"g1", "total": 114},
                { "option": "Option 3", "number": 3, "votes": 9, "group":"g1", "total": 76},
                { "option": "Option 1", "number": 4, "votes": 12, "group":"g2", "total": 63},
                { "option": "Option 2", "number": 5, "votes": 7, "group":"g2", "total": 42},
                { "option": "Option 1", "number": 1, "votes": 3, "group":"g1", "total": 38},
                { "option": "Option 3", "number": 6, "votes": 2, "group":"g2", "total": 21}
                
            ]

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_bordaWrongPath(self):
        """
            * Definición: Test que verifica que obtenemos un not found al realizar
            un post a una página que no existe
            * Entrada: Votación
                - Number: id del partido
                - Option: nombre de la opción
                - Votes: Número de votos que recibe en la votación
                - Group: Grupo de votación al que pertenece
            * Salida: 404, not found
        """        
        data = {
            "type": "BORDA",	
            "options": [
                { "option": "Option 1", "number": 1, "votes": 3, "group":"g1" },
                { "option": "Option 2", "number": 2, "votes": 26, "group":"g1" },
                { "option": "Option 3", "number": 3, "votes": 9, "group":"g1" },
                { "option": "Option 1", "number": 4, "votes": 12, "group":"g2" },
                { "option": "Option 2", "number": 5, "votes": 7, "group":"g2" },
                { "option": "Option 3", "number": 6, "votes": 2, "group":"g2" }  
            ]
        }

        response = self.client.post("/postprocesado/", data, format="json")
        self.assertEqual(response.status_code, 404)
    
    def test_bordaNoType(self):
        """
            * Definición: Test donde no se especifica type en el json de entrada
            * Entrada: Votación
                - Number: id del partido
                - Option: nombre de la opción
                - Votes: Número de votos que recibe en la votación
                - Group: Grupo de votación al que pertenece
            * Salida: los datos de entrada tras aplicarle el type por defecto
            (es decir, la función identity)
        """        
        data = {	
            "options": [
                { "option": "Option 1", "number": 1, "votes": 10, "group":"g1" },
                { "option": "Option 2", "number": 2, "votes": 7, "group":"g1" },
                { "option": "Option 3", "number": 3, "votes": 8, "group":"g1" }
                ]
        }

        expected_result = [
            { "option": "Option 1", "number": 1, "votes": 10, "group":"g1", "postproc":10},
            { "option": "Option 3", "number": 3, "votes": 8, "group":"g1" , "postproc":8},
            { "option": "Option 2", "number": 2, "votes": 7, "group":"g1" , "postproc":7} 
            ]

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_bordaGrupoUnico(self):       
        data = {
            "type": "BORDA",	
            "options": [
                { "option": "Option 1", "number": 1, "votes": 10, "group":"g1" },
                { "option": "Option 2", "number": 2, "votes": 7, "group":"g1" },
                { "option": "Option 3", "number": 3, "votes": 8, "group":"g1" }
                 ]
        }

         
