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
