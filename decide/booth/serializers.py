from rest_framework import serializers

from .models import VotingCount


class VotingCountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VotingCount
        fields = ('id', 'voting_id', 'option_id')
