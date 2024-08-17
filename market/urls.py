from django.urls import path
from . import views


app_name = 'market'


urlpatterns = [
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout_view, name='checkout_view'),
    path('failure/', views.failure_page, name='failure_page'),
    path('success/', views.success_page, name='success_page'),
]
