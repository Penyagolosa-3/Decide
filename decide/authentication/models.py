from django.db import models
from django.db.models.query_utils import Q
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Authentication(models.Model):

    class Rol(models.TextChoices):
        SELLER = 'SE', _('Sheller')
        CLIENT= 'CL', _('Client')

    roles = models.CharField(
        max_length=2,
        choices=Rol.choices,
        default=Rol.CLIENT,
    )
    
    
    class Meta:
        constraints = Q[models.CheckConstraint(check=Q(roles__in=['Sheller', 'Client']), name="valid_roles")]



