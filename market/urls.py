from django.urls import path
from . import views


app_name = 'market'


urlpatterns = [
    path('cart/', views.cart_view, name='cart_view'),
    path('go-gateway/', views.go_to_gateway, name='go_gateway'),
    # path('checkout/', views.checkout_view, name='checkout_view'),
    path('failure/', views.failure_page, name='failure_page'),
    path('success/', views.success_page, name='success_page'),
    path('vrify-trancaction/', views.verify_transaction, name='verify_transaction'),
    path('psp-message/', views.psp_message, name='psp_message'),

]

