from django.shortcuts import redirect
from django.urls import reverse
from django_tenants.utils import get_tenant
from django.contrib import messages


class TenantAdminLockMiddleware:
    def __init__(self, get_respose):
        self.get_response = get_respose

        def __call__(self, request):
            if request.path.startwith("/admin/") and request.user.is_authenticated:
                tenant = get_tenant(request)
                user_email = request.user.email

                if not request.user.username.startswith(tenant.schema_name):
                    messages.error(request, "No tienes permiso para acceder a esta seccion.")
                    return redirect(reverse("admin:logout"))
                
            return self.get_response(request)