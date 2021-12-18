import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import VotingCount
from voting.models import Voting, QuestionOption

from base import mods

class BoothVotingCountView(APIView):
    def post(self, request):
        print(request.data)

        for data in ['option', 'voting']:
            if not data in request.data:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        voting = Voting.objects.get(id=int(request.data.get('voting')))
        option = QuestionOption.objects.get(id=int(request.data.get('option')))

        votingCount = VotingCount(voting = voting, option = option)
        votingCount.save()

        return Response({})

    def get(self, request, voting_id):
        #print(voting_id)
        #voting = Voting.objects.get(id=voting_id)
        votingCount = VotingCount.objects.filter(voting_id=voting_id)
        #print(votingCount.count())
        context = {
            'votingCount': votingCount.values()
        }
        data = json.dumps(context, indent=4, sort_keys=False, default=str)
        return Response(data, content_type='application/json')

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
