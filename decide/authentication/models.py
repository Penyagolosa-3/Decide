from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Rol(models.Model):

    class State(models.IntegerChoices):
        CLIENT= 0, _('Cliente')
        SHELLER = 1, _('Vendedor')

    state = models.IntegerField(default=State.CLIENT, choices=State.choices)