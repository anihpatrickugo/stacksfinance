from django.contrib import admin
from django.urls import path

from .views import (
     HomeView,
     UserDashboardView,

     UserDepositsView,
     UserNewDepositView,

     UserWithdrawalsView,
     UserNewWithdrawalView,

     UserProfileView,
     UserSettingsView,

     UserInvestmentsView,
     UserNewInvestmentView,
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

    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
    path('<int:pk>/proile-settings/', UserSettingsView.as_view(), name='profile-settings'),

    path('investments/', UserInvestmentsView.as_view(), name='investments'),
    path('new-investment/', UserNewInvestmentView.as_view(), name='new-investment'),
]
