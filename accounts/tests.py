from django.test import TestCase, override_settings
from .models import Account, Profile


@override_settings(AXES_ENABLED=True)
class UserModelTest(TestCase):
    def setUp(self):
        self.normal_account = Account.objects.create_user(
            email="testuser@gmail.com", username="testuser", password="123456789"
        )
        self.superuser_account = Account.objects.create_superuser(
            email="testsuperuser@gmail.com",
            username="testsuperuser",
            password="123456789",
        )
        self.user_profile = Profile.objects.get(user=self.normal_account)
        self.user_profile2 = Profile.objects.get(user=self.superuser_account)

    def test_user_is_not_superuser(self):
        self.assertFalse(self.normal_account.is_superuser)

    def test_user_is_superuser(self):
        self.assertTrue(self.superuser_account.is_superuser)

    def test_user_if_not_email(self):
        with self.assertRaises(ValueError):
            account = Account.objects.create_user(
                email="", username="accountuser", password="123456789"
            )

    def test_user_if_not_username(self):
        with self.assertRaises(ValueError):
            account = Account.objects.create_user(
                email="account@gmail.com", username="", password="123456789"
            )

    def test_superuser_is_staff(self):
        with self.assertRaises(ValueError):
            account = Account.objects.create_superuser(
                email="account@email.com",
                username="accountuser",
                password="123456789",
                is_staff=False,
                is_admin=True,
                is_superuser=True,
            )

    def test_superuser_is_superuser(self):
        with self.assertRaises(ValueError):
            account = Account.objects.create_superuser(
                email="account@email.com",
                username="accountuser",
                password="123456789",
                is_staff=True,
                is_admin=True,
                is_superuser=False,
            )

    def test_profile_created_for_user(self):
        self.assertTrue(self.user_profile)

    def test_profile_return_value(self):
        self.assertEqual(
            f"{self.normal_account.username} profile",
            str(self.normal_account.userprofile),
        )

    def test_profile_referal_code_is_unique(self):
        referal_1 = Profile.objects.get(referal_code=self.user_profile.referal_code)
        referal_2 = Profile.objects.get(referal_code=self.user_profile2.referal_code)
        self.assertNotEqual(referal_1, referal_2)

    def test_login(self):
        response = self.client.login(email="testuser@gmail.com", password="123456789")
        self.assertTrue(response)
