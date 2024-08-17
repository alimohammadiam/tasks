from django.shortcuts import render, redirect
from .models import CartItem
from .forms import AddToCartForm
import requests

# Create your views here.


def cart_view(request):
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            CartItem.objects.get_or_create(
                user=request.user,
                product_name=form.cleaned_data['product_name'],
                product_price=form.cleaned_data['product_price'],
                quantity=form.cleaned_data['quantity']
            )
            return redirect('market:cart_view')
    else:
        form = AddToCartForm()

    cart_items = CartItem.objects.filter(user=request.user)
    total_price = (item.total_price() for item in cart_items)

    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'market/cart.html', context)


def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    if request.method == 'POST':
        payment_data = {
            'user': request.user.id,
            'from_market': "market A",
            'amount': float(total_price),
        }

        response = requests.post('http://127.0.0.1:8000/payment/', json=payment_data)

        if response.status_code == 200:
            CartItem.objects.filter(user=request.user).delete()
            return redirect('market:success_page')
        else:
            return redirect('market:failure_page')

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'market/checkout.html', context)


def success_page(request):
    return render(request, 'market/success_page.html')


def failure_page(request):
    return render(request, 'market/failure_page.html')










