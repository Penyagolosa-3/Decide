from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView
from django.contrib import admin

from .views import GetUserView, LogoutView, RegisterView

urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view()),
    path('',TemplateView.as_view(template_name="login.html")),
    path('admin/', admin.site.urls),
    path('accounts/',include('allauth.urls')),
]
