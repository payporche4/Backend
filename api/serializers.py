from rest_framework import serializers
from accounts.models import Account
from app.models import Dashboard, TransactionRecord, Service, MetaTags
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import password_validators_help_texts

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token["id"] = user.id
        # token['username'] = user.username
        return token  # returns refresh token


class MetaTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaTags
        fields = ["metatag", "timestamp"]


class ServiceSerializer(serializers.ModelSerializer):
    user_service = serializers.CharField()

    class Meta:
        model = Service
        fields = [
            "user_service",
            "price",
            "description",
            "category",
            "city",
            "thumbnail",
        ]
        read_only_fields = ["thumbnail"]


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "is_verified"]
        read_only_fields = [
            "is_active",
            "date_joined",
            "last_login",
            "otp",
            "is_verified",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("email", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = ["user", "wallet_balance", "wallet_tag"]


class TransactionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionRecord
        fields = ["sender", "receiver", "amount", "timestamp"]


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()