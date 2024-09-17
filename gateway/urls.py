from django.urls import path
from . import views


app_name = 'gateway'

urlpatterns = [
    # path('payment/', views.TransactionCreate.as_view(), name='payment_gateway'),
    path('payment/', views.payment_page_view, name='payment_page'),
    path('process-payment/', views.process_payment_view, name='proces_payment'),
    path('result/', views.show_bank_result_view, name='show_bank_result'),
    path('return/', views.return_to_market_view, name='return_to_market'),
    path('transaction-status/', views.transaction_status_from_bank, name='transaction_status'),

]
