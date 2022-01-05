from django.shortcuts import redirect
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from .views import GetUserView, LogoutView2, RegisterView, redirection

urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutView2.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view()),
    path('signin/',TemplateView.as_view(template_name="login.html")),
    path('accounts/',include('allauth.urls')),
    path('logoutG', LogoutView.as_view(), name="logoutG"),
    path('redirection', redirection),
]
