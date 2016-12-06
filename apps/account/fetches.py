from community.models import Community, Invitation
from base.forms import *

from django.contrib.auth.models import User

def get_navbar_information(request):
    mod_communities = Community.objects.filter(
        members=request.user,
        membership__is_moderator='True'
    )
    earner_communities = Community.objects.filter(
        members=request.user,
        membership__is_moderator='False'
    )
    return mod_communities, earner_communities

def get_search_form():
    return CommunitySearchForm()


def u_instance(username):
    try:
       username = User.objects.get(username=username)
    except User.DoesNotExist:
       username = None
    return username

def u_pending_invitations(user):
    invitations = Invitation.objects.filter(
        recipient=user,
    ).exclude(
        community__in = Community.objects.filter(
            members=user
        ).values_list('id', flat=True)
    )
    return invitations
