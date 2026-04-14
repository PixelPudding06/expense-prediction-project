from django.contrib import admin
from django.urls import path
from expenses.views import dashboard, add_expense, history, delete_expense, chart, edit_expense

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard),
    path('add/', add_expense),
    path('history/', history),
    path('chart/', chart),
    path('edit/<int:id>/', edit_expense),
    path('delete/<int:id>/', delete_expense),
]