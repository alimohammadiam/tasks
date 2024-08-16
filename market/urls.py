from django.urls import path
from . import views


app_name = 'market'


urlpatterns = [
    path('cart/', views.cart_view, name='cart_view'),
]
