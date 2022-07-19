from django.forms import ValidationError


import pyqrcode
import requests
import json
from pyqrcode import QRCode
from requests.exceptions import ConnectionError

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings

from .forms import DepositForm
from .utils import get_crypto_price



from .models import (
    Investment, 
    Profile, 
    Deposit, 
    Withdrawal, 
    Plan
    )

# Create your views here.

s = settings.BITCOIN_ADDRESS
url = pyqrcode.create(s)
url.png(file='staticfiles\core\img\qrcode.png', scale=6)



    








class HomeView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plans'] = Plan.objects.all()
        return context


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'account/user-dashboard.html'
    login_url = 'account_login'


class UserDepositsView(LoginRequiredMixin, ListView):
    model = Deposit
    template_name = 'account/deposits.html'
    paginate_by = 10
    login_url = 'account_login'

    def get_queryset(self):
        qs = super(UserDepositsView, self).get_queryset()
        qs = qs.filter(user=self.request.user).order_by('-date')
        return qs



class UserNewDepositView(LoginRequiredMixin, CreateView):
    model = Deposit
    template_name = 'account/make-deposit.html'
    form_class = DepositForm
    login_url = 'account_login'
    success_url = reverse_lazy('deposits')
    

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wallet_address'] = settings.BITCOIN_ADDRESS
        context['bitcoin_price'] = get_crypto_price()
        return context







class UserWithdrawalsView(LoginRequiredMixin, ListView):
    model = Withdrawal
    template_name = 'account/withdrawals.html'
    paginate_by = 10
    login_url = 'account_login'

    def get_queryset(self):
        qs = super(UserWithdrawalsView, self).get_queryset()
        qs = qs.filter(user=self.request.user).order_by('-date')
        return qs


class UserNewWithdrawalView(LoginRequiredMixin, CreateView):
    model = Withdrawal
    template_name = 'account/make-withdrawal.html'
    fields = ['amount']
    login_url = 'account_login'
    success_url = reverse_lazy('withdrawals')
    
    

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        if form.instance.amount > self.request.user.balance:
            messages.error(self.request, 'insufficient account balance')
            return self.render_to_response(self.get_context_data(form=form))
          
        return super().form_valid(form)



class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/user-profile.html'


class UserSettingsView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['photo', 'first_name', 'last_name', 'username']
    template_name = 'account/account-settings.html'
    success_url = reverse_lazy('user-profile')


class UserInvestmentsView(LoginRequiredMixin, ListView):
    model = Investment
    template_name = 'account/investments.html'
    paginate_by = 10
    login_url = 'account_login'

    def get_queryset(self):
        qs = super(UserInvestmentsView, self).get_queryset()
        qs = qs.filter(user=self.request.user).order_by('-date')
        return qs


class UserNewInvestmentView(LoginRequiredMixin, CreateView):
    model = Investment
    template_name = 'account/make-investment.html'
    fields = ['plan', 'amount']
    login_url = 'account_login'
    success_url = reverse_lazy('investments')
    
    

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id

        if (form.instance.amount > form.instance.plan.max_amount) or (form.instance.amount < form.instance.plan.min_amount):
            messages.error(self.request, f'Amount must be between {form.instance.plan.min_amount} - {form.instance.plan.max_amount}')
            return self.render_to_response(self.get_context_data(form=form))

        if form.instance.amount > self.request.user.balance:
            messages.error(self.request, 'insufficient account balance for this investment')
            return self.render_to_response(self.get_context_data(form=form))

        
          
        return super().form_valid(form)