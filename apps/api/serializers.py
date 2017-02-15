from django.contrib.auth.models import User
from rest_framework import serializers

from community.models import Community, Membership, Invitation, Application

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Returns a list of all users in the system.
    """
    class Meta:
        model = User
        fields = ('url', 'username', 'email')

class CommunitySerializer(serializers.HyperlinkedModelSerializer):
    """
    Returns a list of all communities in the system.
    """
    class Meta:
        model = Community
        fields = ('name', 'description', 'tag', 'is_private', 'created_on', 'members', 'invitations', 'applications')

