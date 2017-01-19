from community.models import Community, Invitation
from account.models import Profile
from base.forms import *

from community.fetches import *
from badge.fetches import *

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

# Return list of badge classes earnable by users in format:
# [[community1, [badge1, badge2, ...]], [community2, [...]], ...]
def u_earnable_instances_by_community(user):
    retval = []

    user_communities = u_communities(user)
    for x in user_communities:
        earnable_badges = []

        # Get user's status:
        mem = u_membership(x, user)
        community_role = mem.user_status

        # Get all badge classes from that community:
        avail_badgeclasses = all_available_badge_classes(x)

        # Go over each badge class:
        for b in avail_badgeclasses:
            if b.earnable_by == community_role:
                earnable_badges.append(b)

        # Add this community and its badges to retval:
        retval.append([x, earnable_badges])

    return retval

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