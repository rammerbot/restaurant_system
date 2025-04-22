from django_tenants.models import TenantMixin, DomainMixin
from django.db import models



# Clase Base para los registros de creacion de modelos.
class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="Creado", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Actualizado", auto_now=True)

    class Meta:
        abstract = True

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        app_label = 'app'

    # obligatorio
    auto_create_schema = True

class Domain(DomainMixin):
    class Meta:
        app_label = 'app'
