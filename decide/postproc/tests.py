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
                - Option: Nombre de la opción
                - Votes: Número de votos que recibe en la votación
                - Group: Grupo de votación al que pertenece
            * Salida: Los datos de entrada con un nuevo parámetro llamado total
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

    def testParidadError(self):
        """
            * Definicion: Test negativo por URL errónea
            * Entrada: Votacion (Json)
                - Option: Nombre del partido
                - Number: Id de la opcion
                - Votes: Numero de votos de esa votacion
                - PostProc: Numero de personas que van a ir en la lista una vez aplicada la paridad
                - Candidatos: Sexo e ID de los candidatos
            * Salida: Codigo 404
        """
        data = {
            'type': 'PARIDAD',
            'options': [
                {'option': 'Partido Unico', 'number': 1, 'votes': 5, 'postproc': 5, 'candidatos': [
                 {'sexo': 'hombre', 'id': '1'}, {'sexo': 'mujer', 'id': '2'}, {
                     'sexo': 'hombre', 'id': '3'}, {'sexo': 'mujer', 'id': '4'}, {'sexo': 'mujer', 'id': '5'}
                 ]}
            ]
        }

        response = self.client.post('/postproci/', data, format='json')
        self.assertEqual(response.status_code, 404)
    
    def testParidadCorrecto(self):
        """
            * Definicion: Test positivo para una votacion que cumple la paridad
            * Entrada: Votacion (Json)
                - Option: Nombre del partido
                - Number: Id de la opcion
                - Votes: Numero de votos de esa votacion
                - PostProc: Numero de personas que van a ir en la lista una vez aplicada la paridad
                - Candidatos: Sexo e ID de los candidatos
            * Salida: Codigo 200 y json de la paridad
        """
        data = {
            'type': 'PARIDAD',
            'options': [
                {'option': 'Partido Unico', 'number': 1, 'votes': 5, 'postproc': 5, 'candidatos': [
                 {'sexo': 'hombre', 'id': '1'}, {'sexo': 'mujer', 'id': '2'}, {
                     'sexo': 'hombre', 'id': '3'}, {'sexo': 'mujer', 'id': '4'}, {'sexo': 'mujer', 'id': '5'}
                 ]}

            ]
        }


        expected_result = [
            {'option': 'Partido Unico', 'number': 1, 'votes': 5, 'postproc': 5, 'candidatos': [
                {'sexo': 'hombre', 'id': '1'}, {'sexo': 'mujer', 'id': '2'}, {
                    'sexo': 'hombre', 'id': '3'}, {'sexo': 'mujer', 'id': '4'}, {'sexo': 'mujer', 'id': '5'}
            ],
                'paridad': [
                {'sexo': 'mujer', 'id': '2'}, {'sexo': 'hombre', 'id': '1'}, {
                    'sexo': 'mujer', 'id': '4'}, {'sexo': 'hombre', 'id': '3'}, {'sexo': 'mujer', 'id': '5'}
            ]}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def testParidad1Elemento(self):
        """
            * Definicion: Test positivo con solo un candidato de todos los posibles
            * Entrada: Votacion (Json)
                - Option: Nombre del partido
                - Number: Id de la opcion
                - Votes: Numero de votos de esa votacion
                - PostProc: Numero de personas que van a ir en la lista una vez aplicada la paridad
                - Candidatos: Sexo e ID de los candidatos
            * Salida: Codigo 200 y json de la paridad
        """
        data = {
            'type': 'PARIDAD',
            'options': [
                {'option': 'Partido Unico', 'number': 1, 'votes': 5, 'postproc': 1, 'candidatos': [
                 {'sexo': 'hombre', 'id': '1'}, {'sexo': 'mujer', 'id': '2'}, {
                     'sexo': 'hombre', 'id': '3'}, {'sexo': 'mujer', 'id': '4'}, {'sexo': 'mujer', 'id': '5'}
                 ]}
            ]
        }

        expected_result = [
            {'option': 'Partido Unico', 'number': 1, 'votes': 5, 'postproc': 1, 'candidatos': [
                {'sexo': 'hombre', 'id': '1'}, {'sexo': 'mujer', 'id': '2'}, {
                    'sexo': 'hombre', 'id': '3'}, {'sexo': 'mujer', 'id': '4'}, {'sexo': 'mujer', 'id': '5'}
            ],
                'paridad': [
                {'sexo': 'mujer', 'id': '2'}
            ]}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def testParidadCorrecto2(self):
        """
            * Definicion: Test positivo con 2 hombres y 3 mujeres
            * Entrada: Votacion (Json)
                - Option: Nombre del partido
                - Number: Id de la opcion
                - Votes: Numero de votos de esa votacion
                - PostProc: Numero de personas que van a ir en la lista una vez aplicada la paridad
                - Candidatos: Sexo e ID de los candidatos
            * Salida: Codigo 200 y json de la paridad
        """
        data = {
            'type': 'PARIDAD',
            'options': [
                { 'option': 'Partido Unico', 'number': 1, 'votes': 5 , 'postproc': 5, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'mujer','id':'5'}
                ]}
            ]
        }

        expected_result = [
            { 'option': 'Partido Unico', 'number': 1, 'votes': 5, 'postproc': 5, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'mujer','id':'5'}
                ],
                'paridad': [
                 {'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'5'}
                ]}
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def testParidadCorrecto3(self):
        """
            * Definicion: Test positivo con 3 hombres y 2 mujeres
            * Entrada: Votacion (Json)
                - Option: Nombre del partido
                - Number: Id de la opcion
                - Votes: Numero de votos de esa votacion
                - PostProc: Numero de personas que van a ir en la lista una vez aplicada la paridad
                - Candidatos: Sexo e ID de los candidatos
            * Salida: Codigo 200 y json de la paridad
        """
        data = {
            'type': 'PARIDAD',
            'options': [
                { 'option': 'Partido Unico', 'number': 1, 'votes': 5 , 'postproc': 5, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'hombre','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'mujer','id':'5'}
                ]}
            ]
        }

        expected_result = [
            { 'option': 'Partido Unico', 'number': 1, 'votes': 5, 'postproc': 5, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'hombre','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'mujer','id':'5'}
                ],
                'paridad': [
                 {'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'5'}
                ,{'sexo':'hombre','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ]}
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_bordaWrongPath(self):
        """
            * Definición: Test que verifica que obtenemos un not found al realizar
            un post a una página que no existe
            * Entrada: Votación
                - Number: id del partido
                - Option: Nombre de la opción
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
                - Option: Nombre de la opción
                - Votes: Número de votos que recibe en la votación
                - Group: Grupo de votación al que pertenece
            * Salida: Los datos de entrada tras aplicarle el type por defecto
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
    
    def test_dhondt(self):
        
        data = {
            "type": "DHONDT",
            "seats": 8,
            "options": [
                { "option": "Option 1", "number": 1, "votes": 5 },
                { "option": "Option 2", "number": 2, "votes": 0 },
                { "option": "Option 3", "number": 3, "votes": 3 },
                { "option": "Option 4", "number": 4, "votes": 2 },
                { "option": "Option 5", "number": 5, "votes": 5 },
                { "option": "Option 6", "number": 6, "votes": 1 },
            ]
        }

        expected_result = [
            { "option": "Option 1", "number": 1, "votes": 5, "postproc": 3 },
            { "option": "Option 5", "number": 5, "votes": 5, "postproc": 3 },
            { "option": "Option 3", "number": 3, "votes": 3, "postproc": 1 },
            { "option": "Option 4", "number": 4, "votes": 2, "postproc": 1 },
            { "option": "Option 2", "number": 2, "votes": 0, "postproc": 0 },
            { "option": "Option 6", "number": 6, "votes": 1, "postproc": 0 },
        ]

        data = {
            "type": "DHONDT",
            "seats": 10,
            "options": [
                { "option": "Option 1", "number": 1, "votes": 20 },
                { "option": "Option 2", "number": 2, "votes": 11 },
                { "option": "Option 3", "number": 3, "votes": 0 },
                { "option": "Option 4", "number": 4, "votes": 10 },
                { "option": "Option 5", "number": 5, "votes": 5 },
            ]
        }
        
        expected_result = [
            { "option": "Option 1", "number": 1, "votes": 20, "postproc": 5 },
            { "option": "Option 2", "number": 2, "votes": 11, "postproc": 2 },
            { "option": "Option 4", "number": 4, "votes": 10, "postproc": 2 },
            { "option": "Option 5", "number": 5, "votes": 5, "postproc": 1 },
            { "option": "Option 3", "number": 3, "votes": 0, "postproc": 0 },
        ]
   
        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
        
    def test_bordaGrupoUnico(self):
        """
            * Definición: Test donde solo existe un grupo de votación
            * Entrada: Votación
                - Number: id del partido
                - Option: Nombre de la opcion
                - Votes: Número de votos que recibe en la votación
                - Group: Grupo de votación al que pertenece
            * Salida: Los datos de entrada con un nuevo parámetro llamado total
            que supone el valor de esa opción tras aplicar el algoritmo
        """        
        data = {
            "type": "BORDA",	
            "options": [
                { "option": "Option 1", "number": 1, "votes": 10, "group":"g1" },
                { "option": "Option 2", "number": 2, "votes": 7, "group":"g1" },
                { "option": "Option 3", "number": 3, "votes": 8, "group":"g1" }
                 ]
        }

        expected_result = [

                { "option": "Option 1", "number": 1, "votes": 10, "group":"g1", "total":75 },
                { "option": "Option 3", "number": 3, "votes": 8, "group":"g1", "total": 50},
                { "option": "Option 2", "number": 2, "votes": 7, "group":"g1", "total":25}   
            ]

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_dhondt_error(self):
        """
            * Definicion: Test negativo que no recibe escaños
            * Entrada: Votacion
                - Number: id del partido
                - Option: nombre de la opcion
                - Votes: Numero de votos que recibe en la votación
            * Salida: Codigo 200 con mensaje de que no hay escaños suficientes para repartir
        """

        data = {
            "type": "DHONDT",
            "seats": 0,
            "options": [
                { "option": "Option 1", "number": 1, "votes": 10 },
                { "option": "Option 2", "number": 2, "votes": 0 },
                { "option": "Option 3", "number": 3, "votes": 0 },
                { "option": "Option 4", "number": 4, "votes": 1 },
                { "option": "Option 5", "number": 5, "votes": 4 },
                { "option": "Option 6", "number": 6, "votes": 2 },
            ]
        }
         
        expected_result = {
            'message': 'Los escaños son insuficientes'
        }
        
        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_bordaNoGroup(self):
        """
            * Definición: Test donde los votos no están agrupados
            * Entrada: Votación
                - Number: id del partido
                - Option: Nombre de la opción
                - Votes: Número de votos que recibe en la votación
            * Salida: Mensaje de error, indicando que no es posible
            agrupar los votos
        """

        data = {
            "type": "BORDA",	
            "options": [
                { "option": "Option 1", "number": 1, "votes": 5},
                { "option": "Option 2", "number": 2, "votes": 10},
                { "option": "Option 3", "number": 3, "votes": 7},
                { "option": "Option 1", "number": 4, "votes": 8},
                { "option": "Option 2", "number": 5, "votes": 3},
                { "option": "Option 3", "number": 6, "votes": 2} 
            ]
        }

        expected_result = {'message': 'Los votos no se pueden agrupar'}

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_dhondt_mal(self):
        """
            * Definicion: Test negativo que no recibe escaños
            * Entrada: Votacion
                - Number: id del partido
                - Option: nombre de la opcion
                - Votes: Numero de votos que recibe en la votación
            * Salida: Codigo 404
        """

        data = {
            "type": "DHONDT",
            "options": [
                { "option": "Option 1", "number": 1, "votes": 10 },
                { "option": "Option 2", "number": 2, "votes": 0 },
                { "option": "Option 3", "number": 3, "votes": 0 },
                { "option": "Option 4", "number": 4, "votes": 1 },
                { "option": "Option 5", "number": 5, "votes": 4 },
                { "option": "Option 6", "number": 6, "votes": 2 },
            ]
        }
           
        response = self.client.post('/postproci/', data, format='json')
        self.assertEqual(response.status_code, 404)

    def test_dhondt_noVotes(self):
        """
            * Definición: Test negativo que no recibe votos
            * Entrada: Votación
                - Number: id del partido
                - Option: nombre de la opción
                - Votes: Numero de votos que recibe en la votación
            * Salida: Código 200 con los datos de entrada junto con el postprocesado, de forma
            que ningún partido recibe escaños
        """

        data = {
            "type": "DHONDT",
            "seats": 8,
            "options": [
                { "option": "Option 1", "number": 1, "votes": 0 },
                { "option": "Option 2", "number": 2, "votes": 0 },
                { "option": "Option 3", "number": 3, "votes": 0 },
                { "option": "Option 4", "number": 4, "votes": 0 },
                { "option": "Option 5", "number": 5, "votes": 0 },
                { "option": "Option 6", "number": 6, "votes": 0 },
            ]
        }
         
        expected_result = {
            'message': 'No hay votos'
        }
   
        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_bordaPos2(self):
        """
            * Definición: Test que verifica que el algoritmo borda funciona correctamente
            con más opciones y más grupos de votación
            * Entrada: Votación
                - Number: id de la opción
                - Option: Nombre de la opción
                - Votes: Número de votos que recibe en la votación
                - Group: Grupo de votación al que pertenece
            * Salida: Los datos de entrada con un nuevo parámetro llamado total
            que supone el valor de esa opción tras aplicar el algoritmo
        """        

        data = {
            "type": "BORDA",	
            "options": [
                { "option": "Option 1", "number": 1, "votes": 105, "group":"g1" },
                { "option": "Option 2", "number": 2, "votes": 453, "group":"g1" },
                { "option": "Option 3", "number": 3, "votes": 242, "group":"g1" },
                { "option": "Option 1", "number": 4, "votes": 67, "group":"g2" },
                { "option": "Option 2", "number": 5, "votes": 23, "group":"g2" },
                { "option": "Option 3", "number": 6, "votes": 45, "group":"g2" },
                { "option": "Option 1", "number": 7, "votes": 230, "group":"g3" },
                { "option": "Option 2", "number": 8, "votes": 334, "group":"g3" },
                { "option": "Option 3", "number": 9, "votes": 234, "group":"g3" }
                
            ]
        }
        expected_result = [
                { "option": "Option 2", "number": 2, "votes": 453, "group":"g1", "total":2400},
                { "option": "Option 2", "number": 8, "votes": 334, "group":"g3", "total":2394},
                { "option": "Option 3", "number": 3, "votes": 242, "group":"g1", "total":1600},
                { "option": "Option 3", "number": 9, "votes": 234, "group":"g3", "total":1596},
                { "option": "Option 1", "number": 1, "votes": 105, "group":"g1", "total":800},
                { "option": "Option 1", "number": 7, "votes": 230, "group":"g3", "total":798},
                { "option": "Option 1", "number": 4, "votes": 67, "group":"g2","total":405},
                { "option": "Option 3", "number": 6, "votes": 45, "group":"g2", "total":270},
                { "option": "Option 2", "number": 5, "votes": 23, "group":"g2", "total":135}
                
            ]
<<<<<<< HEAD


        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)   
=======


        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)        
        
>>>>>>> c8c80318256ee0c89ea639090ff4b3f9a2b9a5ec
