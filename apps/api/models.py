from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

def replace_auth_token(user):
    try:
        tkn = Token.objects.get(
            user=user
        )
        tkn.delete()
        tkn = Token.objects.create(user=user)
        tkn.save()
    except:
        return False

    return tkn