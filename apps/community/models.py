from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.conf import settings
from django.apps import apps

class Community(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    tag = models.CharField(max_length=10)
    is_private = models.BooleanField(default=False)
    created_on = models.DateField(default=datetime.now)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership',
        related_name='community_members', through_fields=('community', 'user'))
    invitations = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Invitation',
        related_name='community_invitations', through_fields=('community', 'recipient'))
    applications = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Application',
        related_name='community_applications', through_fields=('community', 'applicant'))

    def get_badge_classes(self):
        bc = apps.get_model('badge', 'BadgeClass')
        badge_classes = bc.objects.filter(
            community=self,
        )
        return badge_classes
    # 
    # def get_badge_instances(self, user):
    #     bi = apps.get_model('badge', 'BadgeInstance')
    #     badge_instances = bi.objects.filter(
    #         badge_class__community=self,
    #
    #     )



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

## COMMUNITY REQUESTS (INVITES AND APPLICATIONS) ##
class AbstractRequest(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    created_on = models.DateField(default=datetime.now)
    # accepted_on = models.DateField()

    class Meta:
        abstract = True

class Invitation(AbstractRequest):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='invitation_recipient')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='invitation_sender')
    to_be_moderator = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'invitation'
        verbose_name_plural = 'invitations'
        db_table = 'invitation'

    def __str__(self):
        return self.recipient.username

class Application(AbstractRequest):
    accepted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='application_accepted_by', blank=True, null=True)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='application_applicant')

    class Meta:
        verbose_name = 'application'
        verbose_name_plural = 'applications'
        db_table = 'application'

    def __str__(self):
        return self.applicant.username
