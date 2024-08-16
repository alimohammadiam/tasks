from django import forms


class AddToCartForm(forms.Form):
    product_name = forms.CharField(max_length=250)
    product_price = forms.CharField(max_length=20)
    quantity = forms.IntegerField(min_value=1, initial=1)
