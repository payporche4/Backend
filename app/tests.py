from django.test import TestCase, override_settings
from .models import Category, Dashboard, TransactionRecord, MetaTags, Service
from accounts.models import Account
from .utils import generate_transaction_reference

# Test without AXES Functionality
@override_settings(AXES_ENABLED=False)
class Appapp(TestCase):
    def setUp(self):
        self.create_user = Account.objects.create_user(
            email="tess@gmail.com", username="tess", password="123456789"
        )
        # test_fund_balance = self.create_user.dashboard.wallet_balance + 500
        self.create_user2 = Account.objects.create_user(
            email="teslim@gmail.com", username="teslim", password="123456789"
        )
        self.test_dashboard1 = Dashboard.objects.get(user=self.create_user)
        self.test_dashboard2 = Dashboard.objects.get(user=self.create_user2)
        self.category = Category.objects.create(category="sport")

    def test_dashboard_return_value(self):
        self.assertEqual(f"{self.test_dashboard1}", "tess's Dashboard")

    def test_default_wallet_balance(self):
        self.assertEqual(self.test_dashboard1.wallet_balance, 0.00)

    def test_generate_transaction_reference(self):
        ref = generate_transaction_reference()
        self.assertTrue(ref)

    def test_transaction_amount(self):
        # add funds to test user 1 for transaction purposes
        self.test_dashboard1.wallet_balance += 300
        self.test_dashboard1.save()
        self.transaction = TransactionRecord.objects.create(
            sender=self.test_dashboard1.user,
            receiver=self.test_dashboard2.user,
            amount=50,
            transaction_remark="test transaction",
        )
        self.assertEqual(f"{self.transaction}", str(self.transaction))

    def test_category_return_value(self):
        self.assertEqual(f"{self.category}", str(self.category))

    def test_metatag_return_value(self):
        self.metatag = MetaTags.objects.create(metatag="sport")
        self.assertEqual(f"{self.metatag}", str(self.metatag))

    def test_service_return_value(self):
        self.service = Service.objects.create(
            user=self.create_user,
            price=20,
            description="test description",
            category=self.category,
        )
        self.assertEqual(f"{self.service}", str(self.service))
