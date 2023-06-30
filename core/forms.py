
from allauth.account.forms import SignupForm
from django_countries.fields import CountryField

from django import forms
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.conf import settings

from .models import *
from .validators import age_validator



class SimpleSignupForm(SignupForm):
    first_name      = forms.CharField(max_length=40)
    last_name       = forms.CharField(max_length=40)
    nationality     = CountryField(blank_label= 'Select country').formfield()
    date_of_birth   = forms.DateField(label='Date of Birth',
                                      validators= [age_validator],
                                      initial= datetime.date.today(),
                                      widget=forms.widgets.DateInput(attrs={
                                          'type': 'date'}))
    bitcoin_address = forms.CharField(max_length=40, label='Bitcoin Address')
    referral_code   = forms.CharField(max_length=6, label='Referral Code', required=False,
                                      widget=forms.TextInput(attrs={'placeholder': '--optional--'}))


    field_order = ['username', 'first_name', 'last_name', 'email', 'nationality',
                   'date_of_birth', 'bitcoin_address', 'referral_code']
        

    def clean_referral_code(self):
        code = self.cleaned_data['referral_code']
        referrer = Profile.objects.filter(referral_code=code)

        if code != "":
             if referrer.exists():
                pass
             else:
                raise forms.ValidationError("Referral code does not exist")

        return code

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)

        code            = self.cleaned_data['referral_code']
        nationality     = self.cleaned_data['nationality']
        date_of_birth   = self.cleaned_data['date_of_birth']
        bitcoin_address = self.cleaned_data['bitcoin_address']
        

        if code != '':
            referrer = Profile.objects.get(referral_code=code)

            make_referrals = Referrals.objects.create(referred_by=referrer, referred=user)
            make_referrals.save()
        
        user.nationality = nationality
        user.date_of_birth = date_of_birth
        print(date_of_birth)
        user.bitcoin_address = bitcoin_address
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


   





class ContactForm(forms.Form):
    name     = forms.CharField(widget=forms.TextInput(attrs={'id': 'name', 'placeholder': 'Your Name', 'class': 'form-control'}))
    email    = forms.EmailField(widget=forms.TextInput(attrs={'id': 'emai', 'placeholder': 'Your Email', 'class': 'form-control'}))
    subject  = forms.CharField(widget=forms.TextInput(attrs={'id': 'subject',  'placeholder': 'Subject', 'class': 'form-control'}))
    message  = forms.CharField(widget=forms.Textarea(attrs={'id': 'message',  'placeholder': 'Message', 'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']

        if  '@' not in email:

            print("incorect email format")
            messages.error(self.request, 'incorrect email format')
            raise forms.ValidationError('incorrect email format')
        
        return email