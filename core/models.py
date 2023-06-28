
import datetime

from django_countries.fields import CountryField
from cloudinary.models import CloudinaryField

from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib import messages
from django.conf import settings
from django.urls import reverse


# Create your models here.

class Profile(AbstractUser):
    bitcoin_address = models.CharField(max_length=40)
    # photo = models.ImageField(upload_to='profile_photos', null=True, blank=True)
    photo = CloudinaryField('profile_photos')
    balance = models.PositiveIntegerField(default=0)
    nationality = CountryField(blank_label='select country')
    referral_code = models.CharField(max_length=6, unique=True, blank=True, null=True)


class Referrals(models.Model):
    referred_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    referred = models.OneToOneField(Profile, related_name='owner', on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'referral'

    def __str__(self):
        return f"{self.referred_by} referring {self.referred}"


class Deposit(models.Model):
    user             =   models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount           =   models.IntegerField(default=0)
    trnx_hash        =   models.CharField(max_length=50)
    verified         =   models.BooleanField(default=False)
    date             =   models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return f"{self.user} deposit of ${self.amount}"



class Withdrawal(models.Model):
    user             =   models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount           =   models.IntegerField(default=0, validators=[MinValueValidator(settings.MINIMUM_WITHDRAWAL_AMAOUNT)])
    verified         =   models.BooleanField(default=False)  
    date             =   models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return f"{self.user} withdrawal of ${self.amount}"

  
            
    
        
class Plan(models.Model):

    name       = models.CharField(max_length=50)
    intrest    = models.IntegerField()
    min_amount = models.IntegerField()
    max_amount = models.IntegerField(null=True, blank=True)
    duration   = models.DurationField()
       
    def __str__(self):
        return self.name

    def modified_duration(self):
        return self.duration.days

    def invest_now(self):
        return reverse('invest-now', kwargs={'pk': self.pk})


class Investment(models.Model):
    user       =   models.ForeignKey(Profile, on_delete=models.CASCADE)
    plan       =   models.ForeignKey(Plan, on_delete=models.CASCADE )
    amount     =   models.IntegerField(default=0)
    date       =   models.DateTimeField(auto_now_add=True)
    paid       =   models.BooleanField(default=False)
   
    
       
    def __str__(self):
        return f"{self.user} investment of ${self.amount}"


    def clean(self):
        if (self.amount < self.plan.min_amount) or (self.amount > self.plan.max_amount):
            raise ValidationError(f'Amount must be between ${self.plan.min_amount} - ${self.plan.max_amount}')
        
        super(Investment, self).clean()

    # this returns a datetime.datetime object of the pay date
    def pay_date(self):
        date = self.date + self.plan.duration
        return date
   
   
    @property
    def roi(self):
        profit = (self.plan.intrest/100)*(self.amount)
        total = self.amount + profit
        return total
    
    
    def due_for_payment(self):
        year = int(self.pay_date().strftime("%Y"))
        month = int(self.pay_date().strftime("%m"))
        day = int(self.pay_date().strftime("%d"))
        hour = int(self.pay_date().strftime("%H"))
        min = int(self.pay_date().strftime("%M"))
        sec = int(self.pay_date().strftime("%S"))


        paydate = datetime.datetime(year,month,day,hour,min,sec)
        
        if datetime.datetime.now() >= paydate:
            if self.paid == False:
                 user = Profile.objects.get(pk=self.user.pk)
                 user.balance += (self.roi + self.amount)
                 user.save()
                 self.paid = True
                 self.save()

            return True
        else:
            return False
    
        
 


            