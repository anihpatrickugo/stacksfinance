from django.contrib import admin
from django.contrib import messages


from.models import (
    Profile, 
    Referrals, 
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
admin.site.register(Referrals)
admin.site.register(Deposit)
admin.site.register(Withdrawal)
admin.site.register(Plan)
admin.site.register(Investment, InvestmentAdmin)