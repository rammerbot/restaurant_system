from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from django.contrib.auth import get_user_model
from applications.app.models import Client
from applications.users.models import CustomUser



class Command(BaseCommand):
    help = 'Crea un administrador para un tenant especifico'

    def add_arguments(self, parser):
        parser.add_argument('--schema', type=str, help='Nombre del schema del tenant')
        parser.add_argument('--username', type=str, help= 'Nombre del usuario admin')
        parser.add_argument('--email', type=str, help='Email del admin')
        parser.add_argument('--password', type=str, help='Contraseña del admin')

    def handle(self, *args, **kwargs):
        schema = kwargs['schema']
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password']

        tenant = Client.objects.get(schema_name=schema)
        with tenant_context(tenant):
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                role='TENANT_ADMIN',
                is_staff=True,
                tenant=tenant
            )
            self.stdout.write(self.style.SUCCESS(f'Admin {username} creado en el tenant {schema}'))