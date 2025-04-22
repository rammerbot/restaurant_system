from django.db import models
from django.conf import settings

from applications.client.models import Dish
from applications.app.models import BaseModel
from applications.client.models import Table

# Create your models here.
class Order(BaseModel):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    order_number = models.IntegerField(verbose_name="Numero de orden")
    order_date = models.DateTimeField(verbose_name="Fecha de orden", auto_now_add=True)
    waiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_paid = models.BooleanField(verbose_name="Pagado", default=False)
    is_delivered = models.BooleanField(verbose_name="Entregado", default=False)

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Cantidad", default=1)
    note = models.TextField(verbose_name="Nota", blank=True, null=True)

    def __str__(self):
        return f"{self.dish.name} x {self.quantity}"
