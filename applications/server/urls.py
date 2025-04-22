from django.urls import path
from .views import OrderCreateView

app_name = 'server'
urlpatterns = [
    path('create_order/', OrderCreateView.as_view(), name='create_order'),
   
]