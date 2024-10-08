from django import forms


class BankAccountInfo(forms.Form):
    account_number = forms.CharField(max_length=16, min_length=16, required=True)
    cvv2 = forms.CharField(max_length=4, min_length=4, required=True)
    password = forms.CharField(max_length=128,  required=True, widget=forms.PasswordInput)
    decryption = forms.CharField(widget=forms.Textarea, required=False)
