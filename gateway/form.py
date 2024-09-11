from django import forms


class BankAccountInfo(forms.Form):
    account_number = forms.CharField(max_length=16, required=True)
    cvv2 = forms.CharField(max_length=4, required=True)
    password = forms.CharField(max_length=128, required=True)
    decryption = forms.CharField(widget=forms.Textarea, required=False)
