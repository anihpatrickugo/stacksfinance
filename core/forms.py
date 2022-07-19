from cProfile import label
from email.policy import default
from re import M
from allauth.account.forms import SignupForm
from django import forms
from .models import *


class SimpleSignupForm(SignupForm):
    first_name = forms.CharField(max_length=40, label='First name')
    last_name = forms.CharField(max_length=40, label='Last name')

    bitcoin_address = forms.CharField(max_length=40, label='Bitcoin Address')
   
    def save(self, request):
        user = super(SimpleSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.bitcoin_address = self.cleaned_data['bitcoin_address']
        
        user.save()
        return user
    

class DepositForm(forms.ModelForm):
    bitcoin_value = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'id': 'bitcoin_value'}))

    class Meta:
        model = Deposit
        fields = ['amount', 'bitcoin_value', 'trnx_hash']

        widgets = {
            'amount' : forms.TextInput(attrs={'class': 'form-label', 'id': 'amount', 'oninput': 'mult()', }),
            'trnx_hash' : forms.TextInput(attrs={'class': 'form-label'}),
        }

    def __init__(self, *args, **kwargs):
        super(DepositForm, self).__init__(*args, **kwargs)
        self.fields['bitcoin_value'].initial = self.fields['amount'].initial




    