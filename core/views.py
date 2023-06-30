from datetime import datetime
import pyqrcode


from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect 
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string



from .forms import DepositForm, ContactForm
from .models import (
    Investment, 
    Profile, 
    Deposit,
    Referrals, 
    Withdrawal, 
    Plan
    )

# Create your views here.

s = settings.BITCOIN_ADDRESS
url = pyqrcode.create(s)
url.png(file='staticfiles\core\img\qrcode.png', scale=6)


class HomeView(FormView):
    template_name = 'core/index.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plans'] = Plan.objects.all()
        return context

    def form_valid(self, form):
        self.send_mail(form.cleaned_data)
        messages.success(self.request, 'Your response was submited successfuly.')
        return super().form_valid(form)


    def send_mail(self, valid_data):

        name    = self.request.POST['name']
        subject = self.request.POST['subject']
        html_message = render_to_string('core/email/contact-response.html', {'name':name})
        plain_message = strip_tags(html_message)
        email = self.request.POST['email']
        message = self.request.POST['message']

        from_email    = settings.WEBSITE_DEFAULT_SENDER_EMAIL
        to_emails     = settings.WEBSITE_ADMIN_EMAILS

        send_mail('stacksfinance', plain_message, from_email, [email], html_message=html_message, fail_silently=True)
        send_mail(f'stacksfinance- admin(subject: {subject})', message, from_email, to_emails, fail_silently=True)


   





class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'account/user-dashboard.html'
    login_url = 'account_login'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deposits'] = Deposit.objects.filter(user=self.request.user, verified=True)
        context['withdrawals'] = Withdrawal.objects.filter(user=self.request.user, verified=True)
        context['investments'] = Investment.objects.filter(user=self.request.user)
        context['referrals'] = Referrals.objects.filter(referred_by=self.request.user, paid=True)

        deposit_total    = Deposit.objects.filter(user=self.request.user, verified=True).values_list('amount', flat=True)
        withdrawal_total = Withdrawal.objects.filter(user=self.request.user, verified=True).values_list('amount', flat=True)
        investment_total = Investment.objects.filter(user=self.request.user).values_list('amount', flat=True)
        referral_total   = Referrals.objects.filter(referred_by=self.request.user, paid=True).count()
        
        
        context['deposits_total'] = sum(deposit_total)
        context['withdrawals_total'] = sum(withdrawal_total)
        context['investments_total'] = sum(investment_total)
        context['referrals_total'] = (referral_total)*(settings.SITE_REFERRAL_BONUS)
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wallet_address'] = settings.BITCOIN_ADDRESS
        return context
    

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        self.send_email(form.cleaned_data)
        return super().form_valid(form)

   

    def send_email(self, valid_data):

        name          = self.request.user.username
        nationality   = self.request.user.nationality.name
        amount        = self.request.POST['amount']
        trnx_hash     = self.request.POST['trnx_hash']
        date          = datetime.now()
        html_message  = render_to_string('core/email/new-deposit-alert.html', {'name':name, 'amount':amount, 'trnx_hash':trnx_hash, 'nationality':nationality, 'date':date})
        plain_message = strip_tags(html_message)
        from_email    = settings.WEBSITE_DEFAULT_SENDER_EMAIL
        to_emails     = settings.WEBSITE_ADMIN_EMAILS
        
        
        send_mail('StacksFinance-New Deposit Alert!', plain_message, from_email, to_emails, html_message=html_message, fail_silently=True)
        



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
        
        self.send_email(form.cleaned_data)
        return super().form_valid(form)


    def send_email(self, valid_data):

        name          = self.request.user.username
        nationality   = self.request.user.nationality.name
        amount        = self.request.POST['amount']
        btcn_addr     = self.request.user.bitcoin_address
        date          = datetime.now()
        html_message  = render_to_string('core/email/new-withdrawal-alert.html', {'name':name, 'amount':amount, 'btcn_addr':btcn_addr, 'nationality':nationality, 'date':date})
        plain_message = strip_tags(html_message)
        from_email    = settings.WEBSITE_DEFAULT_SENDER_EMAIL
        to_emails     = settings.WEBSITE_ADMIN_EMAILS
        
        
        send_mail('StacksFinance-New Withdrawal Alert!', plain_message, from_email, to_emails, html_message=html_message, fail_silently=True)




class PlanInvestNowView(View):
    def get(self, request, pk):
        request.session['plan_pk'] = pk
        return redirect('new-investment')

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
            if form.instance.plan.max_amount == None:
                messages.error(self.request, f'Amount must be between {form.instance.plan.min_amount} and unlimited')

            messages.error(self.request, f'Amount must be between {form.instance.plan.min_amount} - {form.instance.plan.max_amount}')
            return self.render_to_response(self.get_context_data(form=form))



            

        if form.instance.amount > self.request.user.balance:
            messages.error(self.request, 'insufficient account balance for this investment')
            return self.render_to_response(self.get_context_data(form=form))

        return super().form_valid(form)


    def get_initial(self):
        initial_values = super(UserNewInvestmentView, self).get_initial()

        try:
            initial_values['plan'] = Plan.objects.get(pk=self.request.session.get('plan_pk'))
            del self.request.session['plan_pk']
        except:
            pass
        return initial_values





class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/user-profile.html'



class UserReferralsView(LoginRequiredMixin, ListView):
    model = Referrals
    template_name = 'account/referrals.html'
    paginate_by = 10
    login_url = 'account_login'

    def get_queryset(self):
        qs = super(UserReferralsView, self).get_queryset()
        qs = qs.filter(referred_by=self.request.user).order_by('-date')
        return qs

   


class UserSettingsView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['photo', 'first_name', 'last_name', 'username', 'bitcoin_address', 'nationality', 'date_of_birth']
    template_name = 'account/account-settings.html'
    success_url = reverse_lazy('user-profile')



class TermsOfServiceView(TemplateView):
    template_name = 'core/terms-of-service.html'

class PrivacyPolicyView(TemplateView):
    template_name = 'core/privacy-policy.html'