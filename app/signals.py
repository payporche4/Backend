from .models import Dashboard
from accounts.models import Profile
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.userprofile.save()


@receiver(post_save, sender=User)
def create_dashboard(sender, instance, created, **kwargs):
	if created:
		Dashboard.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_dashboard(sender, instance, **kwargs):
	instance.userdashboard.save()
