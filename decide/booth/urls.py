from django.urls import path

from .views import BoothView, BoothVotingCountView
from . import views

urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('voting', views.votings),
    path('votingCount/', BoothVotingCountView.as_view()),
    path('votingCount/<int:voting_id>/', BoothVotingCountView.as_view())
]
