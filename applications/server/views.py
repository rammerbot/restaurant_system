from django.views.generic import FormView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.db.models import Prefetch

from .models import Order, OrderItem
from applications.client.models import Category, Dish
from .forms import OrderCreateForm

class OrderCreateView(FormView):
    template_name = 'server/order_form.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('server:create_order')  # o al success view que uses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context['form']

        # Trae categorías con sus platos
        categories = Category.objects.prefetch_related(
            Prefetch('dish_set', queryset=Dish.objects.all())
        )

        # Construye una lista de categorías -> lista de items con sus campos
        categorized_dishes = []
        for category in categories:
            items = []
            for dish in category.dish_set.all():
                qty_field = form[f'dish_{dish.id}_quantity']
                note_field = form[f'dish_{dish.id}_note']
                items.append({
                    'dish': dish,
                    'qty_field': qty_field,
                    'note_field': note_field,
                })
            if items:
                categorized_dishes.append({
                    'category': category,
                    'items': items,
                })

        context['categorized_dishes'] = categorized_dishes
        return context

    def form_valid(self, form):
        table = form.cleaned_data['table']

        if table.is_available:
            table.is_available = False
            table.save()

        order = Order.objects.create(
            table=table,
            order_number=Order.objects.filter(table=table).count() + 1,
            waiter=self.request.user
        )

        # Procesa cada plato según cantidad > 0
        for dish in Dish.objects.all():
            q = form.cleaned_data.get(f'dish_{dish.id}_quantity', 0)
            n = form.cleaned_data.get(f'dish_{dish.id}_note', '')
            if q and q > 0:
                OrderItem.objects.create(order=order, dish=dish, quantity=q, note=n)

        return redirect(self.get_success_url(), order_id=order.id)