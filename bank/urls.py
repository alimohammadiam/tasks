from django.urls import path
from . import views

app_name = 'bank'

urlpatterns = [
    path('process_payment/', views.bank_transaction_view, name='process_payment'),
    path('verify_transaction/<str:transaction_id>/', views.check_last_ok, name='verify_transaction'),

]
