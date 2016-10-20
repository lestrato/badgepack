from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.conf import settings

class Community(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    tag = models.CharField(max_length=10)
    is_private = models.BooleanField(default=False)
    created_on = models.DateField(default=datetime.now)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership')

    class Meta:
        verbose_name = 'community'
        verbose_name_plural = 'communities'
        db_table = 'community'

    def __str__(self):
        return self.name

class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    joined_on = models.DateField(default=datetime.now)
    is_moderator = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'membership'
        verbose_name_plural = 'memberships'
        db_table = 'membership'

    def __str__(self):
        return self.user.username


# class AbstractUser(models.Model):
#     user = models.CharField(max_length=100)
#     community = models.PositiveIntegerField()
#     joined_on = models.DateField(default=datetime.now)
#
#     class Meta:
#         abstract = True
#
#     def __str__(self):
#         return self.user
#
# class Earner(AbstractUser):
#     class Meta:
#         verbose_name = 'earner'
#         verbose_name_plural = 'earners'
#         db_table = 'earner'
#
#
# class Moderator(AbstractUser):
#     class Meta:
#         verbose_name = 'moderator'
#         verbose_name_plural = 'moderators'
#         db_table = 'moderator'
