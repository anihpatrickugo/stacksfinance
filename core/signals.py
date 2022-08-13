import geocoder
from datetime import datetime

from allauth.account.signals import user_logged_in

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from .models import Deposit, Referrals, Withdrawal, Profile, Investment
from .utils import generate_ref_code


@receiver(post_save, sender=Deposit)
def verify_deposit(sender, instance, created, **kwargs):

    if instance.pk is not None:
         
        if instance.verified == True:
            
            person = Profile.objects.get(pk=instance.user.pk)
            person.balance += instance.amount
            person.save()


@receiver(post_save, sender=Withdrawal)
def verify_withdrawal(sender, instance, created, **kwargs):

    if instance.pk is not None:
         
        if instance.verified == True:
            
            person = Profile.objects.get(pk=instance.user.pk)
            person.balance -= instance.amount
            person.save()


@receiver(post_save, sender=Investment)
def deduct_investment(sender, instance, created, **kwargs):



    if instance.pk is not None:

       person = Profile.objects.get(pk=instance.user.pk)
       person.balance -= instance.amount
       person.save()

       try:
           referral_object = Referrals.objects.get(referred=person)

           if referral_object.paid == False:
              referral_object.paid = True
              referral_object.save()
       except ObjectDoesNotExist:
          pass




@receiver(pre_save, sender=Profile)
def create_user_referral_token(sender, instance, **kwargs):
    if instance.pk is None:
        
        instance.referral_code = generate_ref_code()


@receiver(post_save, sender=Referrals)
def pay_referrer(sender, instance, created, **kwargs):

    if instance.pk is not None and instance.paid:

       referrer = Profile.objects.get(pk=instance.referred_by.pk)
       referrer.balance += settings.SITE_REFERRAL_BONUS
       referrer.save()

  
@receiver(user_logged_in)
def send_email(request, **kwargs):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
     
    user            = request.user
    nationality     = request.user.nationality.name
    addr            = geocoder.ip(ip)
    current_city    = addr.city
    current_country = addr.country
    date            = datetime.now()
    html_message  = render_to_string('core/email/new-login-alert.html', {'user':user, 'current_city':current_city, 'current_country':current_country, 'nationality':nationality, 'date':date})
    plain_message = strip_tags(html_message)

    from_email    = settings.WEBSITE_DEFAULT_SENDER_EMAIL
    to_emails     = settings.WEBSITE_ADMIN_EMAILS
   

    send_mail('StacksFinance-New Login Alert!', plain_message, from_email, to_emails, html_message=html_message, fail_silently=True)
