from community.models import Community, Invitation
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

def u_instance(username):
    try:
       username = User.objects.get(username=username)
    except User.DoesNotExist:
       username = None
    return username

def u_all_invitations(user):
    all_invites = Invitation.objects.filter(
        recipient=user,
    )
    return all_invites
