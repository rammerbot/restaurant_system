from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages

from applications.users.models import CustomUser
from applications.users.forms import CustomUserForm, CustomUserEditForm
from .models import Table, Category, Dish
from .forms import CategoryForm, DishForm


# Clase para definir los permisos de los usuarios
class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Comprueba que el usuario tenga uno de los roles permitidos.
    Define en la subclase `allowed_roles = [...]`
    """

    allowed_roles = []
    def test_func(self):
        return (
            self.request.user.is_authenticated and
            self.request.user.role in self.allowed_roles
        )
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('register:login')
        return redirect('client:home')
    
# Permisos para le administrador del tenant
class TenantAdministratorRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['TENANT_ADMIN']

# Permisos para el cajero 
class CashierRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['CAJERO', 'TENANT_ADMIN']

# Permisos para el mesonero
class WaiterRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['MESONERO','CAJERO', 'TENANT_ADMIN']

# Vista para listar usuarios
class UserListView(TenantAdministratorRequiredMixin, ListView):
    model = CustomUser
    template_name = 'client/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return CustomUser.objects.filter(tenant=self.request.user.tenant).exclude(role='TENANT_ADMIN')
    
# Vista para la pagina principal
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'client/home.html'
    
# ------------------------------------------------------------------------------------------------------------------------------------#

# Vista para crear usuario
class UserCreateView(TenantAdministratorRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'client/user_form.html'
    success_url = reverse_lazy('client:user_list')

    def form_valid(self, form):
        form.instance.tenant = self.request.user.tenant
        form.instance.is_staff = False
        form.instance.is_superuser = False
        messages.success(self.request, '✅ Usuario creado exitosamente')  # Mensaje de éxito
        return super().form_valid(form)
    

# Vista para Editar usuario
class UserUpdateView(TenantAdministratorRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserEditForm
    template_name = 'client/user_form.html'
    success_url = reverse_lazy('client:user_list')

    def get_queryset(self):
        return CustomUser.objects.filter(tenant=self.request.user.tenant).exclude(role='TENANT_ADMIN')
    
    def form_valid(self, form):
        form.instance.is_staff = False
        form.instance.is_superuser = False
        messages.success(self.request, '✅ Actualizacion de usuario exitoso')  # Mensaje de éxito
        return super().form_valid(form)
    
# Vista para eliminar usuario
class UserDeleteView(TenantAdministratorRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'client/user_delete.html'
    success_url = reverse_lazy('client:user_list')

    def get_queryset(self):
        return CustomUser.objects.filter(tenant=self.request.user.tenant).exclude(role='TENANT_ADMIN')
    
#-------------------------------------------------------------------------------------------------------------------------------------#

# Vista para crear Mesa
class TableRegisterView(TenantAdministratorRequiredMixin, CreateView):
    model = Table
    fields = '__all__'
    template_name = 'client/create_table.html'
    success_url = reverse_lazy('client:table_list_admin')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '✅ Mesa creada exitosamente')  # Mensaje de éxito
        return response

# Vista para editar mesa
class TableUpdateView(TenantAdministratorRequiredMixin, UpdateView):
    model = Table
    fields = '__all__'
    template_name = 'client/create_table.html'
    success_url = reverse_lazy('client:table_list_admin')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '✅ Mesa Actualizada correctamente')  # Mensaje de éxito
        return response

# Vista para listar mesas
class TableListView(TenantAdministratorRequiredMixin, ListView):
    model = Table
    template_name = 'client/table_list_admin.html'
    context_object_name = 'tables'
    ordering = ['number']

# Vista para eliminar mesa
class TableDeleteView(TenantAdministratorRequiredMixin, DeleteView):
    model = Table
    success_url = reverse_lazy('client:table_list_admin')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '✅La Mesa elimino exitosamente')  # Mensaje de éxito
        return response
#-------------------------------------------------------------------------------------------------------------------------------------#

# vista para listar categorias
class CategoryListView(TenantAdministratorRequiredMixin, ListView):
    model = Category
    template_name = 'client/dishes/category_list.html'
    context_object_name = 'categories'

# Vista para crear categoria
class CategoryCreateView(TenantAdministratorRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'client/dishes/category_form.html'
    success_url = reverse_lazy('client:category_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '✅La Mesa elimino exitosamente')  # Mensaje de éxito
        return response

# Vista para editar categoria
class CategoryUpdateView(TenantAdministratorRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'client/dishes/category_form.html'
    success_url = reverse_lazy('client:category_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '✅La Mesa elimino exitosamente')  # Mensaje de éxito
        return response

# Vista para eliminar categoría
class CategoryDeleteView(TenantAdministratorRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('client:category_list')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': '✅ Categoría eliminada exitosamente'
            })
        
        messages.success(request, '✅ Categoría eliminada exitosamente')
        return redirect(self.get_success_url())
#-------------------------------------------------------------------------------------------------------------------------------------#

# Vista para listar platos
class DishListView(TenantAdministratorRequiredMixin, ListView):
    model = Dish
    template_name = 'client/dishes/dish_list.html'
    context_object_name = 'dishes'

# Vista para crear plato
class DishCreateView(TenantAdministratorRequiredMixin, CreateView):
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
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '✅El Plato/Bebida ha sido creado exitosamente')  # Mensaje de éxito
        return response

# Vista para editar plato
class DishUpdateView(TenantAdministratorRequiredMixin, UpdateView):
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
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '✅El Plato/Bebida ha sido Actualizado exitosamente')  # Mensaje de éxito
        return response

# Vista para eliminar plato
class DishDeleteView(TenantAdministratorRequiredMixin, DeleteView):
    model = Dish
    success_url = reverse_lazy('client:dish_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        return redirect(self.success_url)