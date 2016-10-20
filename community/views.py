from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render
from community.models import Community, Membership

@login_required
def community(request, community_tag):
    mod_communities = Community.objects.filter(members__id=request.user.id, membership__is_moderator='True')
    earner_communities = Community.objects.filter(members__id=request.user.id, membership__is_moderator='False')
    community = get_object_or_404(Community, tag=community_tag)
    all_members = community.members.all()
    membership = Membership.objects.filter(
        community_id=community.id,
        user_id=request.user.id,
    )
    moderator = membership.filter(
        is_moderator='True'
    )
    # member = community.members.filter(id=request.user.id)

    return render_to_response('community.html', {
        'mod_communities': mod_communities,
        'earner_communities': earner_communities,
        'username': request.user.username,
        'all_members' : all_members,
        'is_member' : membership.count()==1,
        'is_moderator' : moderator.count()==1,
        'community': community,
    })
