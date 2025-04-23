from django.urls import path
from . import views

app_name = 'salesreport'
urlpatterns = [
    path('sales-report/', views.SalesReportView.as_view(), name='sales_report'),
]