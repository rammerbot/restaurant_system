from django import forms
from applications.client.models import Table
from applications.users.models import CustomUser

# Formulario para generar reportes de ventas
class SalesReportForm(forms.Form):
    start_date = forms.DateField(
        label='Fecha inicial',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        label='Fecha final',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    PERIOD_CHOICES = [
        ('daily', 'Diario'),
        ('weekly', 'Semanal'),
        ('monthly', 'Mensual'),
        ('annual', 'Anual'),
    ]
    period = forms.ChoiceField(
        label='Agrupar por',
        choices=PERIOD_CHOICES,
        initial='daily',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    table = forms.ModelChoiceField(
        queryset=Table.objects.none(),
        label="Filtrar por mesa",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    waiter = forms.ModelChoiceField(
        queryset=CustomUser.objects.none(),
        label="Filtrar por mesero",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            tenant = user.tenant
            self.fields['table'].queryset = Table.objects.all()
            self.fields['waiter'].queryset = CustomUser.objects.filter(
                tenant=tenant, 
            )