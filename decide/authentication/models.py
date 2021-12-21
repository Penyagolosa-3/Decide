
from django.db import models

class Rol(models.Model):
    # Constants in Model class
    CLIENTE = 'CL'
    VENDEDOR = 'SH'
    USERTYPES = (
        (CLIENTE, 'CL'),
        (VENDEDOR, 'SH'),
    )
    usertypes = models.CharField(
        max_length=1,
        choices=USERTYPES,
        default=CLIENTE,
    )

