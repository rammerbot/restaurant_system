

from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.db.models import Sum, F, DecimalField, Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Sum, F, DecimalField

from applications.client.models import Table
from applications.server.models import Order, OrderItem
from applications.client.models import Table


# Login
class CustomLoginView(LoginView):
    template_name = 'register/login.html'  

# Vista para listar mesas
class TableListView(ListView):
    model = Table
    template_name = 'register/table_list.html'
    context_object_name = 'tables'
    
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'order_set'
        ).annotate(
            active_orders_count=Count('order', 
                filter=Q(order__is_paid=False) | Q(order__is_delivered=False))
        )
    
    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id')
        table_id = request.POST.get('table_id')
        action = request.POST.get('action')
        
        try:
            if action == 'pay_all':
                # Lógica para cobrar todas las órdenes de la mesa
                table = Table.objects.get(id=table_id)
                orders_to_pay = table.order_set.filter(is_paid=False)
                
                for order in orders_to_pay:
                    order.is_paid = True
                    order.save()
                
                messages.success(request, f'Todas las órdenes de {table} marcadas como pagadas')
                
                # Verificar estado actualizado de la mesa
                active_orders_exist = table.order_set.filter(
                    Q(is_paid=False) | Q(is_delivered=False)
                ).exists()
                
                if not active_orders_exist:
                    table.is_available = True
                    table.save()
                else:
                    table.is_available = False
                    table.save()
                
                return redirect('register:table_list')
            
            # Lógica original para acciones individuales
            order = Order.objects.get(id=order_id)
            table = order.table
            
            if action == 'mark_paid':
                order.is_paid = True
                messages.success(request, f'Orden {order.order_number} marcada como pagada')
            elif action == 'mark_delivered':
                order.is_delivered = True
                messages.success(request, f'Orden {order.order_number} marcada como entregada')
            
            order.save()
            
            # Actualizar estado de la mesa
            active_orders_exist = Order.objects.filter(
                table=table
            ).filter(
                Q(is_paid=False) | Q(is_delivered=False)
            ).exists()
            
            if not active_orders_exist:
                table.is_available = True
            else:
                table.is_available = False
            table.save()
            
        except Order.DoesNotExist:
            messages.error(request, 'La orden no existe')
        except Table.DoesNotExist:
            messages.error(request, 'Mesa no encontrada')
        
        return redirect('register:table_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tables_data = []
        
        for table in context['tables']:
            active_orders = table.order_set.filter(
                Q(is_paid=False) | Q(is_delivered=False)
            ).prefetch_related('orderitem_set__dish')
            
            table_total = 0
            for order in active_orders:
                order.items = order.orderitem_set.annotate(
                    total_price=F('quantity') * F('dish__price')
                )
                order.total = order.items.aggregate(
                    total=Sum('total_price', output_field=DecimalField())
                )['total'] or 0
                table_total += order.total
            
            tables_data.append({
                'table': table,
                'active_orders': active_orders,
                'table_total': table_total
            })
        
        context['tables_data'] = tables_data
        return context

#-----------------------------------------------------------------------------------------------------------------------#

class TableActiveOrdersView(DetailView):
    model = Table
    template_name = 'server/table_active_orders.html'
    context_object_name = 'table'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = self.get_object()

        # Obtener órdenes activas (no pagadas y no entregadas) para esta mesa
        active_orders = Order.objects.filter(
            table=table,
            is_paid=False,
            is_delivered=False
        )

        # Obtener todos los ítems de esas órdenes
        active_items = OrderItem.objects.filter(order__in=active_orders).annotate(
            total_price=F('quantity') * F('dish__price')
        )

        # Total general a pagar
        total_amount = active_items.aggregate(
            total=Sum('total_price', output_field=DecimalField())
        )['total'] or 0

        context['active_orders'] = active_orders
        context['active_items'] = active_items
        context['total_amount'] = total_amount

        return context

