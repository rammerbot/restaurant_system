from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect

from applications.users.models import CustomUser
from applications.users.forms import CustomUserForm
from .models import Table, Category, Dish
from .forms import CategoryForm, DishForm


# Crear usuario segun el rol.
class TenantAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'TENANT_ADMIN' and \
                self.request.user.is_authenticated
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('register:login')
        return redirect('client:user_list')
    
# Vista para listar usuarios
class UserListView(TenantAdminRequiredMixin, ListView):
    model = CustomUser
    template_name = 'client/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return CustomUser.objects.filter(tenant=self.request.user.tenant).exclude(role='TENANT_ADMIN')
    
# ------------------------------------------------------------------------------------------------------------------------------------#

# Vista para crear usuario
class UserCreateView(TenantAdminRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'client/user_form.html'
    success_url = reverse_lazy('client:user_list')

    def form_valid(self, form):
        form.instance.tenant = self.request.user.tenant
        form.instance.is_staff = False
        form.instance.is_superuser = False
        return super().form_valid(form)

# Vista para Editar usuario
class UserUpdateView(TenantAdminRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'client/user_form.html'
    success_url = reverse_lazy('client:user_list')

    def get_queryset(self):
        return CustomUser.objects.filter(tenant=self.request.user.tenant).exclude(role='TENANT_ADMIN')
    
    def form_valid(self, form):
        form.instance.is_staff = False
        form.instance.is_superuser = False
        return super().form_valid(form)
    
# Vista para eliminar usuario
class UserDeleteView(TenantAdminRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'client/user_delete.html'
    success_url = reverse_lazy('client:user_list')

    def get_queryset(self):
        return CustomUser.objects.filter(tenant=self.request.user.tenant).exclude(role='TENANT_ADMIN')
    
#-------------------------------------------------------------------------------------------------------------------------------------#

# Vista para crear Mesa
class TableRegisterView(TenantAdminRequiredMixin, CreateView):
    model = Table
    fields = '__all__'
    template_name = 'client/create_table.html'
    success_url = reverse_lazy('client:table_list')

# Vista para editar mesa
class TableUpdateView(TenantAdminRequiredMixin, UpdateView):
    model = Table
    fields = '__all__'
    template_name = 'client/create_table.html'
    success_url = reverse_lazy('client:table_list_admin')

# Vista para listar mesas
class TableListView(TenantAdminRequiredMixin, ListView):
    model = Table
    template_name = 'client/table_list_admin.html'
    context_object_name = 'tables'

# Vista para eliminar mesa
class TableDeleteView(TenantAdminRequiredMixin, DeleteView):
    model = Table
    template_name = 'client/table_confirm_delete.html'
    success_url = reverse_lazy('client:table_list_admin')

#-------------------------------------------------------------------------------------------------------------------------------------#

# vista para listar categorias
class CategoryListView(TenantAdminRequiredMixin, ListView):
    model = Category
    template_name = 'client/dishes/category_list.html'
    context_object_name = 'categories'

# Vista para crear categoria
class CategoryCreateView(TenantAdminRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'client/dishes/category_form.html'
    success_url = reverse_lazy('client:category_list')

# Vista para editar categoria
class CategoryUpdateView(TenantAdminRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'client/dishes/category_form.html'
    success_url = reverse_lazy('client:category_list')

# Vista para eliminar categoria
class CategoryDeleteView(TenantAdminRequiredMixin, DeleteView):
    model = Category
    template_name = 'client/dishes/category_confirm_delete.html'
    success_url = reverse_lazy('client:category_list')
    context_object_name = 'category'

#-------------------------------------------------------------------------------------------------------------------------------------#

# Vista para listar platos
class DishListView(TenantAdminRequiredMixin, ListView):
    model = Dish
    template_name = 'client/dishes/dish_list.html'
    context_object_name = 'dishes'

# Vista para crear plato
class DishCreateView(TenantAdminRequiredMixin, CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'client/dishes/dish_form.html'
    success_url = reverse_lazy('client:dish_list')
    
    def get_form_kwargs(self):
        # Pasamos el request al formulario
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)

# Vista para editar plato
class DishUpdateView(TenantAdminRequiredMixin, UpdateView):
    model = Dish
    form_class = DishForm
    template_name = 'client/dishes/dish_form.html'
    success_url = reverse_lazy('client:dish_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_queryset(self):
        # Filtramos solo los platos del tenant
        return Dish.objects.all()

# Vista para eliminar plato
class DishDeleteView(TenantAdminRequiredMixin, DeleteView):
    model = Dish
    template_name = 'client/dishes/dish_confirm_delete.html'
    success_url = reverse_lazy('client:dish_list')