from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email','role', 'tenant')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informacion personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'role', 'tenant')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # filtrar usuarios del mismo tenant
            qs = qs.filter(tenant=request.user.tenant)
        return qs
    
admin.site.register(CustomUser, CustomUserAdmin)