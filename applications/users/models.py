from django.db import models
from django.contrib.auth.models import AbstractUser
from applications.app.models import Client

# Create your models here.

class CustomUser(AbstractUser):
    ROLES = (
        ('TENANT_ADMIN', 'administrador del tenant'),
        ('MESONERO', 'Mesonero'),
        ('CAJERO', 'Cajero')
    )
    role = models.CharField(max_length=20, choices=ROLES, default='MESONERO')
    tenant = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.username
    
