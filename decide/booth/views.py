import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from voting.models import Voting
from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import VotingCount
from voting.models import Voting, QuestionOption
from census.models import Census
from store.models import Vote

from .serializers import VotingCountSerializer

from base import mods

class BoothVotingCountView(APIView):
    # Descripción: endpoint que inserta un voto en el recuento de votos en vivo de una votación
    # HTTP method: POST
    # Entrada:
    ## option: id de la opción votada
    ## voting: id de la votación
    # Salida: ninguna
    def post(self, request):
        for data in ['option', 'voting']:
            if not data in request.data:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        voting_id = int(request.data.get('voting'))

        # Comprobamos que no exista una votación anterior del mismo usuario
        votes = Vote.objects.filter(voting_id=voting_id, voter_id=request.user.id)

        if len(votes)==0:
            voting = Voting.objects.get(id=voting_id)
            option = QuestionOption.objects.get(id=int(request.data.get('option')))

            votingCount = VotingCount(voting = voting, option = option)
            votingCount.save()
        else:
            print('El usuario ya ha votado antes. Omitiendo voto')

        return Response({})

    # Descripción: endpoint que devuelve el recuento de votos en vivo para una votación
    # HTTP method: GET
    # Entrada:
    ## id: id de la votación
    # Salida: matriz con el fetch de los votos realizados a una votación
    def get(self, request, voting_id):
        votingCount = VotingCount.objects.filter(voting_id=voting_id)

        census = Census.objects.filter(voting_id=voting_id)

        votingCount.census = len(census)

        return Response({'votingCount': VotingCountSerializer(votingCount, many=True).data, 'census': len(census)})


# TODO: check permissions and census
class BoothView(TemplateView):
    template_name = 'booth/booth.html'

    def post(self, request, *args, **kwargs):
        print(self.request.POST)
        return HttpResponse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})

            # Casting numbers to string to manage in javascript with BigInt
            # and avoid problems with js and big number conversion
            for k, v in r[0]['pub_key'].items():
                r[0]['pub_key'][k] = str(v)

            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        context['KEYBITS'] = settings.KEYBITS

        return context

def votings(request):
    votings = Voting.objects.exclude(end_date__isnull = False) 
    return render(request, 'booth/votings.html', {'votings': votings})

