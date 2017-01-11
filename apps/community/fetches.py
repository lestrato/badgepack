from django.shortcuts import get_object_or_404

from community.models import Community, Membership, Application, Invitation
from badge.models import BadgeClass, BadgeInstance

def community_object(community_tag):
    # this commounity, based on tag
    try:
       community = Community.objects.get(tag=community_tag)
    except Community.DoesNotExist:
       community = None
    return community

def all_community_applications(community):
    # all community applications
    all_applications = Application.objects.filter(
        community=community,
    )
    return all_applications

def u_application(community, user):
    # user's application
    try:
       application = Application.objects.get(
           community=community,
           applicant=user,
       )
    except Application.DoesNotExist:
       application = None
    return application

def all_community_memberships(community):
    # all community memberships
    all_memberships = Membership.objects.filter(
        community=community,
    )
    return all_memberships

def all_earners(community):
    all_earners = Membership.objects.filter(
      community=community,
      user_status="earner"
    )

    return all_earners
    
def u_membership(community, user):
    # user's membership return first object or none
    try:
       membership = Membership.objects.get(community=community, user=user)
    except Membership.DoesNotExist:
       membership = None
    return membership

def u_invitation(community, user):
    # user's invitation return first object or none
    try:
       invitation = Invitation.objects.get(
           community=community,
           recipient=user,
       )
    except Invitation.DoesNotExist:
       invitation = None
    return invitation

def all_community_invitations(community):
    # all community invitations
    all_invitations = Invitation.objects.filter(
        community=community,
    )
    return all_invitations

def u_communities(members, user_status=None):
    if not user_status:
        communities =  Community.objects.filter(
            members=members,
        )
    else:
        communities = Community.objects.filter(
            members=members,
            membership__user_status=user_status
        )
    return communities
