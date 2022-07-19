from audioop import reverse
from django.contrib import admin
from django.forms import ValidationError
from django.contrib import messages
from django.shortcuts import redirect, render

from.models import (
    Profile, 
    Deposit, 
    Withdrawal, 
    Plan, 
    Investment,
    )




class WithdrwalAdmin(admin.ModelAdmin):


    def save_model(self, request, obj, form, change):
        if obj.amount > obj.user.balance:
            return messages.error(request, 'insufficientadmin account balance for user')
            
            
        return super().save_model(request, obj, form, change)



class InvestmentAdmin(admin.ModelAdmin):

    exclude = ['paid']


    def save_model(self, request, obj, form, change):
        if obj.amount > obj.user.balance:
            return messages.error(request, 'insufficient account balance for user')
            
            
        return super().save_model(request, obj, form, change)


   

    


# Register your models here.
admin.site.register(Profile)
admin.site.register(Deposit)
admin.site.register(Withdrawal)
admin.site.register(Plan)
admin.site.register(Investment, InvestmentAdmin)