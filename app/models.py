from django.db import models
from .utils import (
    unique_rand,
    generate_transaction_reference,
    user_thumbnail_folder,
)
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL


class Dashboard(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userdashboard"
    )
    wallet_balance = models.DecimalField(default=0.00, decimal_places=2, max_digits=300)
    wallet_tag = models.CharField(unique=True, max_length=16)

    def __str__(self):
        return f"{self.user.username}'s Dashboard"

    def save(self, *args, **kwargs):
        wallet_tag = unique_rand()
        try:
            Dashboard.objects.get(wallet_tag=wallet_tag)
        except Dashboard.DoesNotExist:
            self.wallet_tag = wallet_tag
        super(Dashboard, self).save(*args, **kwargs)


class TransactionRecord(models.Model):
    reference_id = models.CharField(max_length=13)
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User, related_name="receiver", on_delete=models.CASCADE
    )
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_remark = models.CharField(max_length=300)

    def save(self, *args, **kwargs):
        reference_id = generate_transaction_reference()
        try:
            TransactionRecord.objects.get(reference_id=reference_id)
        except TransactionRecord.DoesNotExist:
            self.reference_id = reference_id
        super(TransactionRecord, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.amount}"


class Category(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = "categories"


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_service"
    )
    price = models.IntegerField()
    description = models.CharField(max_length=200)
    city = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="service_category"
    )
    thumbnail = models.ImageField(
        upload_to=user_thumbnail_folder, verbose_name="thumbnail", blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s service"


class MetaTags(models.Model):
    metatag = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.metatag}"

    class Meta:
        verbose_name_plural = "MetaTags"
