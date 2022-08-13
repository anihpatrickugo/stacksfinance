from django.contrib import admin
from django.urls import path

from .views import (
     HomeView,
     PrivacyPolicyView,
     UserDashboardView,

     UserDepositsView,
     UserNewDepositView,
     UserReferralsView,

     UserWithdrawalsView,
     UserNewWithdrawalView,

     UserProfileView,
     UserSettingsView,
     
     PlanInvestNowView,
     UserInvestmentsView,
     UserNewInvestmentView,

     TermsOfServiceView,
     PrivacyPolicyView
    
)
 


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', HomeView.as_view(), name='login'),
    path('signup/', HomeView.as_view(), name='signup'),
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),

    path('deposits/', UserDepositsView.as_view(), name='deposits'),
    path('new-deposit/', UserNewDepositView.as_view(), name='new-deposit'),

    path('withdrawals/', UserWithdrawalsView.as_view(), name='withdrawals'),
    path('new-withdrawal/', UserNewWithdrawalView.as_view(), name='new-withdrawal'),

    path('investments/', UserInvestmentsView.as_view(), name='investments'),
    path('new-investment/', UserNewInvestmentView.as_view(), name='new-investment'),

    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
    path('<int:pk>/proile-settings/', UserSettingsView.as_view(), name='profile-settings'),

    path('referrals/', UserReferralsView.as_view(), name='referrals'),

    path('invest-now/<int:pk>/', PlanInvestNowView.as_view(), name='invest-now'),

    path('terms-of-service/', TermsOfServiceView.as_view(), name='terms-of-service'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
]
