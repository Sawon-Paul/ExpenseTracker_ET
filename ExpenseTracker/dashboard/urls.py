# transactions/urls.py
from django.urls import path
from .views import transaction_list

urlpatterns = [
    path('transactions/', transaction_list, name='transaction_list'),
]