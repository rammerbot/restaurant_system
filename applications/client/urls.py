from django.urls import path
from . import views


app_name = 'client'
urlpatterns = [
    # Mesas
    path('create_table/', views.TableRegisterView.as_view(), name='create_table'),
    path('table_list_admin/', views.TableListView.as_view(), name='table_list_admin'),
    path('update_table/<pk>', views.TableUpdateView.as_view(), name='update_table'),
    # Users
    path('user_list', views.UserListView.as_view(), name='user_list'),
    path('create_user/', views.UserCreateView.as_view(), name='user_create'),
    path('update_user/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
    path('delete_user/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),
     # Categorías
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/edit/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    # Platillos
    path('dishes/', views.DishListView.as_view(), name='dish_list'),
    path('dish/create/', views.DishCreateView.as_view(), name='dish_create'),
    path('dish/edit/<int:pk>/', views.DishUpdateView.as_view(), name='dish_update'),
    path('dish/delete/<int:pk>/', views.DishDeleteView.as_view(), name='dish_delete'),
]
