from django.urls import *
from rest_framework.test import APITestCase, APIClient
from accounts.models import *
from app.models import *
from rest_framework import status

class APITestCase(APITestCase):
    def setUp(self):
        self.user1 = Account.objects.create_user(
            email="user1@gmail.com", username="user1", password="123456789"
        )
        self.user2 = Account.objects.create_user(
            email="user2@gmail.com", username="user2", password="123456789"
        )
        self.user1_dashboard = Dashboard.objects.get(user=self.user1)
        self.user2_dashboard = Dashboard.objects.get(user=self.user2)
        self.cat = Category.objects.create(category="Tech")

    def test_login_view(self):
        client = APIClient()
        data = {"email": self.user1.email, "password": "123456789"}
        url = reverse("token_obtain_pair")
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_referal_view(self):
        url = reverse(
            ("referal"), kwargs={"ref_code": self.user1.userprofile.referal_code}
        )
        client = APIClient()
        data = {
            "email": "tess@gmail.com",
            "username": "tess",
            "password": "ehis123456",
            "password2": "ehis123456",
        }
        client.post(url, data, format="json")
        new_user = Profile.objects.get(user__email="tess@gmail.com")
        self.assertEqual(new_user.refered_by, self.user1)

    def test_failed_register_view(self):
        url = reverse("apiregister")
        client = APIClient()
        data = {
            "email": "tess@gmail.com",
            "username": "tess",
            "password": "1234",
            "password2": "12345678",
        }
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_view(self):
        url = reverse("change_password")
        client = APIClient()
        client.login(email=self.user1, password="123456789")
        data = {"old_password": "123456789", "new_password": "teslim12345"}
        change_password_response = client.put(url, data, format="json")
        new_login_response = client.login(email=self.user1, password="teslim12345")
        self.assertEqual(change_password_response.status_code, status.HTTP_200_OK)
        self.assertTrue(new_login_response)

    def test_change_password_view_for_wrong_old_password(self):
        url = reverse("change_password")
        client = APIClient()
        client.login(email=self.user1, password="123456789")
        self.assertFalse(self.user1.check_password("12345678"))
        data = {"old_password": "012345678", "new_password": "teslim12jesusisking"}
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_possible_error(self):
        url = reverse("change_password")
        client = APIClient()
        client.login(email=self.user1, password="123456789")
        data = {"old_password": "0123456789", "new_password": ""}
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_dashboard_view(self):
        client = APIClient()
        url = reverse("dashboard")
        client.login(email=self.user1, password="123456789")
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_validate_password_on_referral_view(self):
        url = reverse(
            ("referal"), kwargs={"ref_code": self.user1.userprofile.referal_code}
        )
        data = {
            "username": "testusername",
            "email": "testemail@gmail.com",
            "password": "1234",
            "password2": "1234",
        }
        client = APIClient()
        # with self.assertRaises(ValidationError):
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_does_not_exist_response(self):
        url = reverse(("referal"), kwargs={"ref_code": str(111122)})
        data = {
            "username": "testusername",
            "email": "testemail@gmail.com",
            "password": "jesusisking1234",
            "password2": "jesusisking1234",
        }
        client = APIClient()
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_for_password_dont_match_response(self):
        url = reverse(
            ("referal"), kwargs={"ref_code": self.user1.userprofile.referal_code}
        )
        data = {
            "username": "testusername",
            "email": "testemail@gmail.com",
            "password": "jesusisking1234",
            "password2": "1234",
        }
        client = APIClient()
        # with self.assertRaises(ValidationError):
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_possible_referral_form_error_response(self):
        url = reverse(
            ("referal"), kwargs={"ref_code": self.user1.userprofile.referal_code}
        )
        data = {
            "username": "",
            "email": "testemail@gmail.com",
            "password": "jesusisking1234",
            "password2": "jesusisking1234",
        }
        client = APIClient()
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_passwords(self):
        url = reverse("apiregister")
        data = {
            "username": "testusername",
            "email": "testemail@gmail.com",
            "password": "jesusisking1234",
            "password2": "jesusisking1234",
        }
        client = APIClient()
        response = client.post(url, data, format="json")
        self.assertEqual(data["password"], data["password2"])
        test_account = Account.objects.get(username="testusername")
        self.assertTrue(test_account.check_password("jesusisking1234"))

    def test_registration_passwords_dont_match(self):
        url = reverse("apiregister")
        data = {
            "username": "testusername",
            "email": "testemail@gmail.com",
            "password": "jesusisking1234",
            "password2": "1234",
        }
        client = APIClient()
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_possible_registration_form_error_response(self):
        url = reverse("apiregister")
        # testing with an already registered username, should fail
        data = {
            "username": self.user1.username,
            "email": "testemail@gmail.com",
            "password": "jesusisking1234",
            "password2": "jesusisking1234",
        }
        client = APIClient()
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_otp_view(self):
        """
        this test requires
        1. A new user registring
        2. Getting that user instance
        3. Logging in with the new user instance
        4. verifying this new user with it's email
        and emailed OTP

        we assert the
        - serializer data (verification data)
        - email is equal to the email in the verification data
        - otp is equal to the otp in the verification data
        """
        client = APIClient()
        register_url = reverse("apiregister")
        register_data = {
            "username": "testusername",
            "email": "testemail@gmail.com",
            "password": "jesusisking1234",
            "password2": "jesusisking1234",
        }
        client.post(register_url, register_data, format="json")
        testuser = Account.objects.get(email="testemail@gmail.com")
        client.login(email=testuser.email, password="jesusisking1234")
        verify_url = reverse("verifyotp")
        verify_data = {
            "email": testuser.email,
            "otp": testuser.otp,
        }
        self.assertTrue(verify_data)
        self.assertEqual(verify_data["email"], testuser.email)
        self.assertEqual(verify_data["otp"], testuser.otp)
        response = client.post(verify_url, verify_data, format="json")

    def test_verify_otp_account_does_not_exist(self):
        """
        Should fail if email entered is not in the system
        """
        client = APIClient()
        register_url = reverse("apiregister")
        register_data = {
            "username": "testusername",
            "email": "testemail@gmail.com",
            "password": "jesusisking1234",
            "password2": "jesusisking1234",
        }
        client.post(register_url, register_data, format="json")
        testuser = Account.objects.get(email="testemail@gmail.com")
        client.login(email=testuser.email, password="jesusisking1234")
        verify_url = reverse("verifyotp")
        verify_data = {
            "email": "ehis@blessed.com",
            "otp": testuser.otp,
        }
        response = client.post(verify_url, verify_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_verify_wrong_otp(self):
        """
        Testing for wrong OTP
        """
        client = APIClient()
        register_url = reverse("apiregister")
        register_data = {
            "username": "testusername",
            "email": "testemail@gmail.com",
            "password": "jesusisking1234",
            "password2": "jesusisking1234",
        }
        client.post(register_url, register_data, format="json")
        testuser = Account.objects.get(email="testemail@gmail.com")
        client.login(email=testuser.email, password="jesusisking1234")
        verify_url = reverse("verifyotp")
        verify_data = {
            "email": testuser.email,
            "otp": 23019,
        }
        response = client.post(verify_url, verify_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_is_verified(self):
        """
        Testing User is already verified,
        should return a 304(Not modified) reponse
        """
        client = APIClient()
        register_url = reverse("apiregister")
        register_data = {
            "username": "testusername",
            "email": "testemail@gmail.com",
            "password": "jesusisking1234",
            "password2": "jesusisking1234",
        }
        client.post(register_url, register_data, format="json")
        testuser = Account.objects.get(email="testemail@gmail.com")
        client.login(email=testuser.email, password="jesusisking1234")
        testuser.is_verified = True
        testuser.save()
        verify_url = reverse("verifyotp")
        verify_data = {
            "email": testuser.email,
            "otp": testuser.otp,
        }
        response = client.post(verify_url, verify_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)

    def test_possible_error_with_verifying_otp(self):
        """
        Testing User is already verified,
        should return a 304(Not modified) reponse
        """
        client = APIClient()
        register_url = reverse("apiregister")
        register_data = {
            "username": "testusername",
            "email": "testemail@gmail.com",
            "password": "jesusisking1234",
            "password2": "jesusisking1234",
        }
        client.post(register_url, register_data, format="json")
        testuser = Account.objects.get(email="testemail@gmail.com")
        client.login(email=testuser.email, password="jesusisking1234")
        testuser.is_verified = True
        testuser.save()
        verify_url = reverse("verifyotp")
        verify_data = {
            "email": "somemail",
            "otp": testuser.otp,
        }
        response = client.post(verify_url, verify_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resend_otp(self):
        client = APIClient()
        url = reverse("resendotp")
        client.login(email=self.user1, password="123456789")
        data = {"email": self.user1.email}
        self.assertTrue(data["email"])
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_resend_otp_email_does_not_exist(self):
        client = APIClient()
        url = reverse("resendotp")
        client.login(email=self.user1.email, password="123456789")
        data = {"email": "ehis@blessed.com"}
        # Request resending OTP
        # Fails because email is not registered
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_resend_otp_bad_request(self):
        client = APIClient()
        url = reverse("resendotp")
        client.login(email=self.user1.email, password="123456789")
        data = {"email": "ehis"}
        # Request resending OTP
        # Fails because email is invalid
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_account_view(self):
        client = APIClient()
        reponse = client.login(email=self.user1.email, password="123456789")
        self.assertTrue(reponse)
