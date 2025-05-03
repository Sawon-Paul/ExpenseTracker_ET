# transactions/urls.py
from django.urls import path
from .views import transaction_list
from . import views


urlpatterns = [
    path('transactions/', transaction_list, name='transaction_list'),
    path('notifications/', views.notifications, name='notifications'),
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/<int:id>/', views.budget_detail, name='budget_detail'),  
    path('export/expenses/csv/', views.export_expenses_csv, name='export_expenses_csv'),
    path('export/expenses/pdf/', views.export_expenses_pdf, name='export_expenses_pdf'),
    path('export/expenses/excel/', views.export_expenses_excel, name='export_expenses_excel'),
    path('export/budgets/csv/', views.export_budgets_csv, name='export_budgets_csv'),
    path('export/budgets/pdf/', views.export_budgets_pdf, name='export_budgets_pdf'),
    path('export/budgets/excel/', views.export_budgets_excel, name='export_budgets_excel'),  
]
