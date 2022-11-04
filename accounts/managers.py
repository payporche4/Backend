from django.contrib.auth.models import BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault("is_admin", True)
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser is_staff field should be `True`")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser is_superuser field should be `True`")
        return self.create_user(email, username, password, **other_fields)
