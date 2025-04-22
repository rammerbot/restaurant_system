from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django_tenants.utils import get_tenant
from django.contrib import messages

class TenantAccessMiddleware:
    """
    Middleware para restringir el acceso a los tenants.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar solo si el usuario está autenticado y NO es superusuario
        if request.user.is_authenticated and not request.user.is_superuser:
            current_tenant = get_tenant(request)
            user_tenant = getattr(request.user, "tenant", None)

            # Si el tenant del usuario no coincide con el tenant actual
            if user_tenant != current_tenant:
                logout(request)  # Cerrar sesión
                login_url = reverse("register:login") + f"?error=invalid_tenant"
                messages.error(request, "Usuario no autorizado, verifique las credenciales de acceso.")
                return HttpResponseRedirect(login_url)  # Redirigir al login

        # Continuar con la solicitud si todo está bien
        response = self.get_response(request)
        return response