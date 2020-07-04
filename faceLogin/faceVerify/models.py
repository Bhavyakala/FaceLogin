from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    picture = models.ImageField(upload_to='images/')

@receiver(post_save, sender=User)
def create_profile(sender ,instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
