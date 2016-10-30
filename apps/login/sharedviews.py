from community.models import Community

def get_navbar_information(request):
    mod_communities = Community.objects.filter(
        members__id=request.user.id,
        membership__is_moderator='True'
    )
    earner_communities = Community.objects.filter(
        members__id=request.user.id,
        membership__is_moderator='False'
    )
    return mod_communities, earner_communities
