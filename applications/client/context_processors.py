from .models import Table
from applications.server.models import Order

def table_status(request):
        return {
            'tables_available': Table.objects.filter(is_available=True).count(),
            'tables_unavailable': Table.objects.filter(is_available=False).count()
        }

def orders_status(request):
        return {
            'orders_pending': Order.objects.filter(is_paid=False).count(),
            'orders_undelivered': Order.objects.filter(is_delivered=False).count()
        }