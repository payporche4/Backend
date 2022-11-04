from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.conf import settings
from .utils import generate_referal_code
from .managers import MyAccountManager
User = settings.AUTH_USER_MODEL


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", unique=True, max_length=100)
    username = models.CharField(verbose_name="username", unique=True, max_length=30)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=5, blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userprofile")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True)
    phone_number = models.CharField(max_length=14, blank=True)
    address = models.CharField(max_length=300, blank=True)
    referal_code = models.CharField(max_length=6, unique=True)
    refered_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="refered_by", blank=True, null=True
    )
    dob = models.CharField(max_length=30)

    def save(self, *args, **kwargs):
        referal_code = generate_referal_code()
        try: 
            Profile.objects.get(referal_code=referal_code)
        except Profile.DoesNotExist:
            self.referal_code = referal_code
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} profile"