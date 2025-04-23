from django.views.generic import TemplateView
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncWeek, TruncMonth, TruncYear, TruncDay


from applications.client.models import Table
from applications.users.models import CustomUser
from applications.server.models import Order, OrderItem
from applications.client.views import CashierRequiredMixin

class SalesReportView(CashierRequiredMixin,TemplateView):
    template_name = 'sales_report/sales_report.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener parámetros de filtro
        report_type = self.request.GET.get('report_type', 'daily')
        start_datetime_str = self.request.GET.get('start_datetime')
        end_datetime_str = self.request.GET.get('end_datetime')
        waiter_id = self.request.GET.get('waiter')
        table_id = self.request.GET.get('table')
        
        # Manejo de zona horaria
        tzinfo = timezone.get_current_timezone()
        now = timezone.localtime(timezone.now())

        # Establecer fechas por defecto
        if report_type == 'daily':
            start_datetime = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_datetime = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif report_type == 'weekly':
            start_datetime = (now - timedelta(days=now.weekday())).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            end_datetime = start_datetime + timedelta(days=6, hours=23, minutes=59, seconds=59)
        elif report_type == 'monthly':
            start_datetime = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_datetime = (start_datetime + timedelta(days=32)).replace(day=1) - timedelta(microseconds=1)
        elif report_type == 'yearly':
            start_datetime = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end_datetime = now.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        else:
            start_datetime = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_datetime = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Procesar fechas del formulario
        if start_datetime_str:
            naive_start = datetime.strptime(start_datetime_str, '%Y-%m-%dT%H:%M')
            start_datetime = timezone.make_aware(naive_start, tzinfo)
        
        if end_datetime_str:
            naive_end = datetime.strptime(end_datetime_str, '%Y-%m-%dT%H:%M')
            end_datetime = timezone.make_aware(naive_end, tzinfo)

        # Consulta base
        orders = Order.objects.filter(
            order_date__gte=start_datetime,
            order_date__lte=end_datetime,
            is_paid=True
        ).select_related('waiter', 'table')
        
        # Filtros adicionales
        if waiter_id:
            orders = orders.filter(waiter_id=waiter_id)
        if table_id:
            orders = orders.filter(table_id=table_id)
        
        # Agrupación por periodo
        trunc_map = {
            'daily': TruncDay('order_date'),
            'weekly': TruncWeek('order_date'),
            'monthly': TruncMonth('order_date'),
            'yearly': TruncYear('order_date')
        }
        trunc_func = trunc_map.get(report_type, TruncDay('order_date'))
        
        # Datos para gráficos
        sales_data = orders.annotate(period=trunc_func).values('period').annotate(
            total_sales=Sum(F('orderitem__quantity') * F('orderitem__dish__price')),
            order_count=Count('id', distinct=True)
        ).order_by('period')
        
        # Datos para gráficos y tablas
        sales_data = orders.annotate(period=trunc_func).values('period').annotate(
            total_sales=Sum(F('orderitem__quantity') * F('orderitem__dish__price')),
            order_count=Count('id', distinct=True)
        ).order_by('period')
        
        # Datos por mesa
        table_data = orders.values('table__number').annotate(
            table_name=F('table__number'),
            total_sales=Sum(F('orderitem__quantity') * F('orderitem__dish__price')),
            order_count=Count('id', distinct=True)
        ).order_by('-total_sales')
        
        # Datos por mesero
        waiter_data = orders.values('waiter__username', 'waiter__first_name', 'waiter__last_name').annotate(
            waiter_name=F('waiter__first_name'),
            total_sales=Sum(F('orderitem__quantity') * F('orderitem__dish__price')),
            order_count=Count('id', distinct=True)
        ).order_by('-total_sales')
        
        # Datos por categoría de plato
        category_data = OrderItem.objects.filter(
            order__in=orders
        ).values('dish__category__category').annotate(
            category_name=F('dish__category__category'),
            total_sales=Sum(F('quantity') * F('dish__price')),
            item_count=Sum('quantity')
        ).order_by('-total_sales')
        
        # Datos por plato
        dish_data = OrderItem.objects.filter(
            order__in=orders
        ).values('dish__name', 'dish__price').annotate(
            dish_name=F('dish__name'),
            total_sales=Sum(F('quantity') * F('dish__price')),
            item_count=Sum('quantity')
        ).order_by('-total_sales')[:10]  # Top 10 platos
        
        # Totales generales
        total_sales = orders.aggregate(
            total=Sum(F('orderitem__quantity') * F('orderitem__dish__price'))
        )['total'] or 0
        total_orders = orders.count()
        average_per_order = total_sales / total_orders if total_orders > 0 else 0
        
        context.update({
            'report_type': report_type,
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
            'sales_data': sales_data,
            'table_data': table_data,
            'waiter_data': waiter_data,
            'category_data': category_data,
            'dish_data': dish_data,
            'total_sales': total_sales,
            'total_orders': total_orders,
            'average_per_order': average_per_order,
            'tables': Table.objects.all(),
            'waiters': CustomUser.objects.filter(tenant=self.request.user.tenant),
            'current_waiter': int(waiter_id) if waiter_id else None,
            'current_table': int(table_id) if table_id else None,
        })
        
        return context