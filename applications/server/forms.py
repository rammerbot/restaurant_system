from django import forms
from applications.client.models import Table, Dish, Category


class OrderCreateForm(forms.Form):
    table = forms.ModelChoiceField(
        queryset=Table.objects.all(),
        label="Mesa",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control mb-4'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.prefetch_related('dish_set').all()
        
        for category in categories:
            for dish in category.dish_set.all():
                # Campo para cantidad
                self.fields[f'dish_{dish.id}_quantity'] = forms.IntegerField(
                    label='Cantidad',
                    required=False,
                    min_value=0,
                    initial=0,
                    widget=forms.NumberInput(attrs={
                        'class': 'form-control shadow',
                        'placeholder': '0',
                        'data-dish-id': dish.id
                    })
                )
                
                # Campo para notas
                self.fields[f'dish_{dish.id}_note'] = forms.CharField(
                    label='Nota',
                    required=False,
                    widget=forms.TextInput(attrs={
                        'class': 'form-control shadow',
                        'placeholder': 'Especificaciones...',
                        'data-dish-id': dish.id
                    })
                )