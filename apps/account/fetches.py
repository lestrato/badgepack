from community.models import Community, Invitation
from account.models import Profile
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

def u_public_id(user):
    profile = u_profile(user=user)
    if profile:
        return profile.public_id

    return None

def u_profile(profile_id):
    try:
        u_profile = Profile.objects.get(profile_id=profile_id)
    except Profile.DoesNotExist:
        return None
    return u_profile

def u_profile_by_user(user):
    try:
        u_profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        return None
    return u_profile


# def u_all_invitations(user):
#     all_invites = Invitation.objects.filter(
#         recipient=user,
#     )
#     return all_invites

# def u_pending_invitations(user):
#     pending_invites = Invitation.objects.filter(
#         recipient=user
#     ).exclude(
#         community__in = Community.objects.filter(
#             members=user
#         ).values_list('id', flat=True)
#     )

#     return pending_invites