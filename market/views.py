from django.shortcuts import render, redirect
from .models import CartItem
from .forms import AddToCartForm

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
