from django.db import models
from applications.app.models import BaseModel

# Create your models here.

class Test(BaseModel):
    employee = models.CharField(verbose_name= "Employee", max_length=100, blank=True, null=True)