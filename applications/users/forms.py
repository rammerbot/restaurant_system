from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserForm(UserCreationForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña...'})
    )

    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña...'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electronico...'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre...'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido...'}),
            'role': forms.Select(attrs={'class': 'form-control'})
        }

        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electronico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'role': 'Rol'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].choices = [
            ('MESONERO', 'Mesonero'),
            ('CAJERO', 'Cajero')
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staf = False
        user.is_superuser = False
        if commit:
            user.save()
        return user
    

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico...'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre...'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido...'}),
            'role': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'role': 'Rol'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].choices = [
            ('MESONERO', 'Mesonero'),
            ('CAJERO', 'Cajero')
        ]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = CustomUser.objects.filter(username=username)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Ya existe un usuario con este nombre.")

        return username
