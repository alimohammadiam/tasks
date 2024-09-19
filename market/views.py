import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem, Transaction
from .forms import AddToCartForm
from .serializers import CartItemSerializer
from django.http import JsonResponse
import requests


# Create your views here.


def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            CartItem.objects.get_or_create(
                user=request.user,
                product_name=form.cleaned_data['product_name'],
                product_price=form.cleaned_data['product_price'],
                quantity=form.cleaned_data['quantity'],
                total_price_cart=total_price
            )
            return redirect('market:cart_view')
    else:
        form = AddToCartForm()

    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'market/cart.html', context)


def go_to_gateway(request):
    cart_data = CartItem.objects.filter(user=request.user)
    if not cart_data.exists():
        return JsonResponse({'error': 'Cart is empty'}, status=400)

    # serializer = CartItemSerializer(cart_data, many=True)
    # data = serializer.data

    total_price = float(sum(item.total_price() for item in cart_data))
    product_name = 'Market A'  # فعلا اسم مارکت رو میفرستم چون تعداد زیادی اسم محصول ارسال میشد

    data = {
        'total_price': total_price,
        'product_name': product_name,
    }

    csrf_token = request.COOKIES.get('csrftoken')

    headers = {
        'X-CSRFToken': csrf_token
    }

    response = requests.post('http://127.0.0.1:8000/gateway/payment/', json=data, headers=headers)

    if response.status_code == 200:
        return redirect('http://127.0.0.1:8000/gateway/process-payment/')

    else:
        return JsonResponse({'error': 'Failed to send data to gateway'}, status=500)


def success_page(request):
    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))
        transaction_id = data.get('transaction_id')

        transaction = Transaction.objects.create(
            user=data.get('user'),
            transaction_id=data.get('transaction_id'),
            transaction_result=data.get('transaction_result'),
            reference_id=data.get('reference_id'),
            account_number=data.get('account_number'),
            amount=data.get('amount'),
            status=data.get('status'),
        )

        if data.get('status') == 'success' and verify_transaction(transaction_id):
            send_last_ok(transaction_id)

        return render(request, 'market/success_page.html')
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def verify_transaction(transaction_id):
    # get bank result
    # check product
    # send last oky for psp and bank
    return True


def send_last_ok(transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    transaction.last_market_ok = True
    transaction.save()

    try:
        response = requests.post('http://psp-server/get-ok', json={
            'last_market_ok': True,
            'transaction_id': transaction_id
        })
        if response.status_code != 200:
            raise ValueError('Failed to notify psp')
    except requests.exceptions.RequestException as e:
        print(f'Error sending request to psp : {e}')


def failure_page(request):
    return render(request, 'market/failure_page.html')


def psp_message(request):
    print('a message from psp getting')







