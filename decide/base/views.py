from django.shortcuts import render
from authentication.models import Roll
from base.perms import UserIsStaff
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_409_CONFLICT as ST_409
)

# Create your views here.
class Inicio():
    permission_classes = (UserIsStaff,)

    def create(self, request, *args, **kwargs):
        users = request.data.get('users')
        rol = request.data.get('rol')
        try:
            for vuser in users:
                if (request.GET.get('rol')==''):
                    rol = Roll(request.auth.key, rol)
                    Roll.save()
        except IntegrityError:
            return Response('Error try to create rol', status=ST_409)
        return Response('Rol created', status=ST_201)

   


