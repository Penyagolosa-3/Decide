
from django.db import models

class Rol(models.Model):
    # Constants in Model class
    CLIENTE = 'CL'
    VENDEDOR = 'SH'
    CHOICES = (
        (CLIENTE, 'CL'),
        (VENDEDOR, 'SH'),
    )
    year_in_school = models.CharField(
        max_length=2,
        choices=CHOICES,
        default=CLIENTE,
    )

