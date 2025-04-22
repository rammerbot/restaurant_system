from django.core.management.base import BaseCommand
from applications.app.models import Client, Domain
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Crea un nuevo tenant con dominio'

    def add_arguments(self, parser):
        parser.add_argument('--schema', type=str, required=True, help='Nombre del schema del tenant')
        parser.add_argument('--name', type=str, required=True, help='Nombre del tenant')
        parser.add_argument('--domain_name', type=str, required=True, help='Dominio para el tenant')  # Cambio aquí
        parser.add_argument('--paid_until', type=str, default='2025-12-31', help='Fecha de expiración (YYYY-MM-DD)')

    def handle(self, *args, **options):
        schema_name = options['schema']
        name = options['name']
        domain_name = options['domain_name']
        paid_until = options['paid_until']

        # Verifica si el schema ya existe
        if Client.objects.filter(schema_name=schema_name).exists():
            self.stdout.write(self.style.WARNING(f"⚠️ Ya existe un tenant con el schema '{schema_name}'."))
            return

        # Verifica si el dominio ya está en uso
        if Domain.objects.filter(domain=domain_name).exists():
            self.stdout.write(self.style.WARNING(f"⚠️ El dominio '{domain_name}' ya está en uso."))
            return

        try:
            tenant = Client(schema_name=schema_name, name=name, paid_until=paid_until)
            tenant.save()

            domain = Domain(domain=domain_name, tenant=tenant, is_primary=True)
            domain.save()

            self.stdout.write(self.style.SUCCESS(f"✅ Tenant '{name}' creado con schema '{schema_name}' y dominio '{domain_name}'"))
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f"❌ Error al crear el tenant: {e}"))
