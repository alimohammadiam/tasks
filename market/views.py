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
            return redirect('cart_view')
    else:
        form = AddToCartForm()

    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'market/cart.html', context)


def checkout_view(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.total_price() for item in cart_items)

        payment_data = {
            'user': request.user.id,
            'from_market': 'market A',
            'amount': total_price,
        }

        response = requests.post('http://gateway_app/payment/', json=payment_data)

        if response.status_code == 200:
            CartItem.objects.filter(user=request.user).delete()
            return redirect('success_page')
        else:
            return redirect('failure_page')

    return render(request, 'market/')













