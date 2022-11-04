from django.core.mail import send_mail
from accounts.utils import generate_otp
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


def send_otp_via_email(email, username=None):
    subject = "Account verification mail"
    otp = generate_otp()
    try:
        user_obj = User.objects.get(email=email)
        user_obj.otp = otp
        user_obj.save()
    except Exception as e:
        raise serializers.ValidationError({"email does not exist": str(e)})
    message = f"Hey {username}, your otp is {otp}. Please go back to the website and verify your account!"
    from_mail = "support@payporche.com"
    send_mail(subject, message, from_mail, [email])
