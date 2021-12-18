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
            grp = self.group(options)
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
