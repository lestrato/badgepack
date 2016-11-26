from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.conf import settings
from django.apps import apps
from django.utils import timezone

# class CommunityManager(models.Manager):
#     def edit_description(self, description):
#         self.description=description
#         return self

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
    # objects = CommunityManager()

    def get_badge_classes(self):
        bc = apps.get_model('badge', 'BadgeClass')
        badge_classes = bc.objects.filter(
            community=self,
        )
        return badge_classes

    def edit_description(self, description):
        self.description=description
        return self

    def change_privacy(self, is_private):
        self.is_private=is_private
        return self

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
    USER_STATUS_CHOICES = (
        ('earner', 'earner'),
        ('moderator', 'moderator'),
        ('owner', 'owner'),
    )
    user_status = models.CharField(
        max_length=10,
        choices=USER_STATUS_CHOICES,
        default='earner',
    )

    def edit_permissions(self, permissions):
        self.user_status=permissions
        return self

    class Meta:
        verbose_name = 'membership'
        verbose_name_plural = 'memberships'
        db_table = 'membership'

    def __str__(self):
        return self.user.username

''' COMMUNITY REQUESTS (INVITES AND APPLICATIONS) '''
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

    def edit_permissions(self, permissions):
        self.to_be_moderator=permissions
        return self

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

    def accept(self, accepted_by):
        self.accepted_by=accepted_by
        return self

    class Meta:
        verbose_name = 'application'
        verbose_name_plural = 'applications'
        db_table = 'application'

    def __str__(self):
        return self.applicant.username
