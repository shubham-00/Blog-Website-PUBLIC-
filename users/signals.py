from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    '''
    Whenever a user is saved, then send a signal called 'post_save'
    'create_profile' receives the signal.
    if user is created, then make profile
    '''
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    '''
    Whenever a user is saved, then send a signal called 'post_save'
    'create_profile' receives the signal.
    if user is created, then make profile
    '''
    instance.profile.save()