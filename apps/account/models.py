from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import random
import uuid

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_id = models.CharField(max_length=30)
    profile_id = models.CharField(max_length=256, blank=True, unique=True, default=uuid.uuid4)

    def edit_public_id(self, public_id):
        self.public_id=public_id
        return self

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
        db_table = 'profile'

    def __str__(self):
        return self.public_id

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a profile:
        default_id = get_random_name()
        Profile.objects.create(user=instance, public_id=default_id)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

def get_random_name():
    default_names = [
        "Apple", "Apricot", "Avocado", "Banana", "Blackberry",
        "Blackcurrant", "Blueberry", "Boysenberry", "Currant",
        "Cherry", "Coconut", "Cranberry", "Cucumber", "Dragonfruit",
        "Durian", "Fig", "Gooseberry", "Grape", "Raisin", "Grapefruit",
        "Guava", "Huckleberry", "Jackfruit", "Jujube", "Kiwi",
        "Kumquat", "Lemon", "Lime", "Loquat", "Longan", "Lychee",
        "Mango", "Melon", "Cantaloupe", "Honeydew", "Watermelon",
        "Mulberry", "Olive", "Orange", "Clementine", "Tangerine",
        "Papaya", "Peach", "Pear", "Persimmon", "Plum", "Pineapple",
        "Pomegranate", "Raspberry", "Strawberry", "Tomato", "Feijoa",
        "Chirimoya"
    ]
    return "Anonymous {0}".format(random.choice(default_names))