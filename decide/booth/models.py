from django.db import models

from voting.models import Voting, QuestionOption

# Create your models here.

class VotingCount(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    option = models.ForeignKey(QuestionOption, on_delete=models.CASCADE)