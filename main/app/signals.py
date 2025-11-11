from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)