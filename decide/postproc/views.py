from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def groups(self, options):

        """
            * Definición: Agrupa cada opción segun su grupo de votación
            * Entrada: Json de la votación
            * Salida: Diccionario cuya llave son los grupos de votación y el valor listas de opciones
        """

        groups = set()
        grpOptions = {}

        # Obtención de grupos
        for opt in options:
            groups.add(opt["group"])
        
        # Inicialización de lista de opciones
        for group in groups:
            grpOptions[group] = []
        
        # Categorización de opciones por grupo
        for opt in options:
            grpOptions[opt.get("group")].append(opt)
        
        return grpOptions

    
    def borda(self, options):

        """
            * Definicion: Aplica el algoritmo de recuento Borda
            * Entrada: Json de la votación
            * Salida: Lista de candidatos con un nuevo parámetro que supone el valor de sus votos tras aplicar borda
        """

        # Comprobamos que las opciones tienen el atributo groups, habiendo al menos 2 opciones
        if(len(options) < 2):
            res = {'message': 'No hay opciones suficientes para agrupar'}
        elif not 'group' in options[0]:
            res = {'message': 'Los votos no se pueden agrupar'}
        else:
            for opt in options:
                # Añadimos a todas las opciones el atributo 'total'
                opt['total'] = 0
        
            #Agrupamos las opciones según el grupo de votación al que pertenezcan
            grp = self.groups(options)
            res = []

            for g in grp:
                #Ordenamos las opciones según el número de votos
                lista = sorted(grp[g], key = lambda x:x["votes"])
                votosTotales = 0

                #Obtenemos la suma todos los votos
                for lis in lista:
                    votosTotales +=  lis["votes"]
                
                contador = 1

                # Se aplica el algoritmo de borda
                for l in lista:
                    puntuacion = votosTotales * contador
                    l['total'] = puntuacion
                    res.append(l)
                    contador += 1
                
            # Tras aplicar el algoritmo, se ordenan las opciones según su puntuación total
            res.sort(key=lambda x:x['total'], reverse=True)

        return Response(res) 

    
    def paridad(self, options):
        """
            * Definicion: Devuelve la lista candidatos intercalando hombres y mujeres si se cumple la paridad
            * Entrada: Json de la votacion
            * Salida: Lista de candidatos ordenada si hay paridad, mensaje de error si no hay paridad
        """

        out = []

        for opt in options:
            out.append({
                **opt,
                'paridad': [],
            })

        for i in out:
            escanios = i['postproc']
            candidatos = i['candidatos']
            listaH = []
            listaM = []
            h = 0
            m = 0
            paridad = True

            for candi in candidatos:
                if candi['sexo'] == 'hombre':
                    listaH.append(candi)
                elif candi['sexo'] == 'mujer':
                    listaM.append(candi)

            check = self.checkPorcentajeParidad(listaH, listaM)

            if not check:
                out = {'message': 'No se cumplen los ratios de paridad 60%-40%'}
                break

            while escanios > 0:
                if paridad:
                    if m < len(listaM):
                        i['paridad'].append(listaM[m])
                        m = m + 1
                    else:
                        i['paridad'].append(listaH[h])
                        h = h + 1
                    paridad = False
                 else:
                    
                    if h < len(listaHombres):
                        i['paridad'].append(listaHombres[h])
                        h = h + 1
                   
                    else:
                        i['paridad'].append(listaMujeres[m])
                        m = m + 1
                    paridad = True

                escanios -= 1
        return out

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'BORDA':
            return self.borda(opts)

        return Response({})
