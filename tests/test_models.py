from unittest import TestCase
from django.contrib.auth import get_user_model
from core.models import Profile, Referrals

User = get_user_model()


# class UserTestCase(TestCase):
#     def setup(self):
#         profile = Profile.objects.create(
#             bitcoin_address='jdjdkjdjdjcjcosisposos',
#         )
#
#         user = User.objects.create(
#                  username='anihpatrickugo',
#                  email='iampatrickugo@gmail.com',
#                  profile=None
#         ).set_password('password1234')
#         user.profile = profile
#
#
#     def test_user_exists(self):
#         user = User.objects.get(username='anihpatrickugo')
#
#         # check user exists
#         self.assertIsInstance(user, User, 'this is a user')
#
#         #check user has referral code
#         self.assertIsNotNone(user.referral_code)
#
#         #check user has bitcoin_address
#         self.assertIsNotNone(user.bitcoin_address)
#
#         #check user balance is 0 by default
#         self.assertEqual(user.balance, 0)
#
#         #check that user has a nationality by default
#         self.assertIsNotNone(user.nationality)




class ReferralTestCase(TestCase):
    def setup(self):

        #first user
        user1 = User.objects.create(
            username='anihpatrickugo',
            email='iampatrickugo@gmail.com',
            profile=None
        ).set_password('password1234')

        #setting referral
        referral = Referrals.object.create(referred_by=user1, referred=user1).save()

    def test_referral(self):
        user1 = User.objects.get(username='anihpatrickugo')
        user2 = User.objects.get(username='anihpatrickugo')

        referral_object = Referrals.objects.get(referred=user1)

        #check that user1 actually referred user2
        self.assertEqual(referral_object.referred, user2)


