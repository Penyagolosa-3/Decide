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

            # Almacenamos en dos listas los hombres y las mujeres
            for candi in candidatos:
                if candi['sexo'] == 'hombre':
                    listaH.append(candi)
                elif candi['sexo'] == 'mujer':
                    listaM.append(candi)

            check = self.checkPorcentajeParidad(listaH, listaM)

            if not check:
                out = {'message': 'No se cumplen los ratios de paridad 60%-40%'}
                break

            # Recorremos todos los escanios disponibles
            while escanios > 0:
                # Si existe paridad en ese momento
                if paridad:
                    # Si la cantidad de mujeres incluidas es menor que la cantidad de mujeres
                    if m < len(listaM):
                        i['paridad'].append(listaM[m])
                        m = m + 1
                    # Si no, se aniade un hombre y se pone la paridad a False
                    else:
                        i['paridad'].append(listaH[h])
                        h = h + 1
                    paridad = False

                # Si no existe paridad en ese momento
                else:
                    # Si el numero de hombres es menor que el numero de hombres en la lista, se aniade un hombre
                    if h < len(listaH):
                        i['paridad'].append(listaH[h])
                        h = h + 1
                    # En caso contrario, se aniade una mujer y vuelve a existir paridad en la lista
                    else:
                        i['paridad'].append(listaM[m])
                        m = m + 1
                    paridad = True

                # Cuenta regresiva de los escanios
                escanios -= 1
        return out

    def checkPorcentajeParidad(self, hombres, mujeres):
        """
            * Definicion: Comprueba si se cumplen los porcentajes minimos de hombres y mujeres
            * Entrada: Lista de hombres y de mujeres en la votacion
            * Salida: True si se cumple la paridad, False si no se cumple
        """
        total = len(hombres)+len(mujeres)

        porcentajeHombres = len(hombres)/total
        porcentajeMujeres = len(mujeres)/total

        return not (porcentajeMujeres < 0.4 or porcentajeHombres < 0.4)
    
    def dhondt(self, options, seats):

        """
            * Definicion: Asigna escaños en las listas electorales
            * Entrada: Json de la votación asignando los escaños según corresponda
            * Salida: Lista de la opciones ordenadas según el número de escaños que posean,
            de mayor a menor
        """

        #Para cada opcion se le añaden escaños
        for opt in options:
            opt['postproc'] = 0

        #Para asignar escaños, se realiza la división entre los vosotros que tiene cada opción y los escaños (inicialmente se divide entre 1)
        #El mayor cociente se lleva el escaño
        for i in range(seats):
            max(options, 
                key = lambda x : x['votes'] / (x['postproc'] + 1.0))['postproc'] += 1

        #Se ordenan las opciones según los escaños
        options.sort(key=lambda x: -x['postproc'])
        out = options

        a = len(options)-1
        b = 0
        c = True

        while b < a:
            if(options[b]['votes'] == options[b+1]['votes'] and options[b]['votes'] == 0):
                c = True
            else:
                c=False
                break
            b = b+1
        
        if(seats == 0):
            out = {'message': 'Los escaños son insuficientes'}
        elif(c == True):
            out = {'message': 'No hay votos'}
        elif(len(options) < 2):
            out = {'message': 'No hay opciones suficientes'}

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
        s = request.data.get('seats')

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'BORDA':
            return self.borda(opts)
        elif t == 'PARIDAD':
            return Response(self.paridad(opts))
        elif t == 'DHONDT':
            return Response(self.dhondt(opts, s))

        return Response({})

