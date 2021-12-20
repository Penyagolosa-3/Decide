from django.db import models
from enum import Enum

# Create your models here.
class Rol(Enum):
    Cliente = 1;
    Vendedor = 2;

class Roll(models.Model):
    user_id = models.PositiveIntegerField()
    rol = Rol
