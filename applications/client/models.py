from django.db import models

from applications.app.models import BaseModel

# Create your models here.

# Clase Base para los registros de creacion de modelos.
class Table(BaseModel):
    number = models.IntegerField(verbose_name="Numero de mesa", unique=True)
    is_available = models.BooleanField(verbose_name="Disponible", default=True)
    def __str__(self):
        return f"Mesa {str(self.number)}"

class Category(BaseModel):
    category = models.CharField(verbose_name="Categoria", max_length=100)
    description = models.TextField(verbose_name="Descripcion")
    image = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.category

class Dish(BaseModel):
    name = models.CharField(verbose_name="Nombre", max_length=100, unique=True)
    price = models.DecimalField(verbose_name="Precio", max_digits=10, decimal_places=2)
    description = models.TextField(verbose_name="Descripcion")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='dishes/')

    def __str__(self):
        return self.name
    


