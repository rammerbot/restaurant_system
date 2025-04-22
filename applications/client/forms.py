from django import forms
from .models  import Category, Dish

# Formulario para crear categoria
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category', 'description', 'image']
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'category': 'Categoria',
            'description': 'Descripcion',
            'image': 'Imagen'
        }

# Formulario para crear plato.
class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'price', 'description', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'name': 'Nombre',
            'price': 'Precio',
            'description': 'Descripción',
            'category': 'Categoría',
            'image': 'Imagen'
        }

    def __init__(self, *args, **kwargs):
        # Extraemos el request de los kwargs
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        if self.request and self.request.user.is_authenticated:
            # Filtramos las categorías por tenant del usuario
            self.fields['category'].queryset = Category.objects.all()
            self.fields['category'].empty_label = "Seleccione una categoría"
        else:
            # Si no hay usuario autenticado, no mostrar categorías
            self.fields['category'].queryset = Category.objects.none()
