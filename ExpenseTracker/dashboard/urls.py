# transactions/urls.py
from django.urls import path
from .views import transaction_list, delete_transaction

urlpatterns = [
    path('transactions/', transaction_list, name='transaction_list'),
    path('transactions/<int:transaction_id>/delete/', delete_transaction, name='delete_transaction'),
]