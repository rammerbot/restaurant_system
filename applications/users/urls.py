from django.contrib.auth import views as auth_views
from django.urls import path

app_name = 'users'
urlpatterns = [
    # Otras URLs...
    path('logout/', auth_views.LogoutView.as_view(next_page='register:login'), name='logout'),
]