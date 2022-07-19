
from sqlite3 import IntegrityError
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import Deposit, Withdrawal, Profile, Investment

from django.contrib.auth.models import AbstractUser


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


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Profile.objects.get_or_create(user=instance)
post_save.connect(create_user_profile, sender=AbstractUser)