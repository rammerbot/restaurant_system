
from django.urls import path
from . import views


app_name = 'register'
urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('tables/', views.TableListView.as_view(), name='table_list'),
]
