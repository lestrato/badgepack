from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.http import HttpResponseRedirect

from community.models import Community, Membership, Application
from community.forms import *
from login.sharedviews import get_navbar_information

@login_required
def community(request, community_tag):

    # create membership based on whether the user created it for someone
    # else or for him/herself
    def create_membership(user_type):
        new_membership = Membership(
            user=user_type,
            community=community,
            joined_on=timezone.now(),
            is_moderator=False
        )
        new_membership.save()

    # get information for navbar
    mod_communities, earner_communities = get_navbar_information(request)


    # this commounity, based on tag
    community = get_object_or_404(
        Community,
        tag=community_tag
    )

    # all community applications
    all_applications = Application.objects.filter(
        community=community.id,
    )

    # user's application
    application = Application.objects.filter(
        community=community.id,
        applicant=request.user.id
    )

    # all community memberships
    all_memberships = Membership.objects.filter(
        community=community.id
    )

    # user's membership
    membership = Membership.objects.filter(
        community_id=community.id,
        user_id=request.user.id,
    )

    # user's moderator status
    moderator = membership.filter(
        is_moderator='True'
    )

    # fetch proper template extension based on current permissions
    if moderator:
        extendTemplate = 'moderator.html'
    elif membership:
        extendTemplate = 'earner.html'
    else:
        extendTemplate = 'visitor.html'

    form = UserPermissionForm(request.POST or None)
    if request.method == 'POST':

        print request.POST # TODO:for debugging

        if 'permissionSubmit' in request.POST:
            form = UserPermissionForm(request.POST)
            if form.is_valid():
                user_membership = get_object_or_404(
                    all_memberships,
                    user=request.POST['member']
                )
                user_membership.is_moderator=form.cleaned_data['permissions']
                user_membership.save()

                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/home/'))

        if 'acceptApplication' in request.POST:

            accepted_application = get_object_or_404(
                all_applications,
                applicant=request.POST['acceptApplication']
            )

            accepted_application.accepted_by=request.user
            accepted_application.save()

            create_membership(accepted_application.applicant)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/home/'))

        if 'cancelApplication' in request.POST:
            # check if the application exists
            if application:
                # remove it
                application.filter().first().delete()

                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/home/'))

        if 'communityJoin' in request.POST:
            # check if community is private or not
            if community.is_private:
                # check if user has been invited to this community

                # check if user already submitted an application to this community
                if application:
                    print "User already created an application to this community"
                # if neither, create new application
                else:
                    new_application = Application(
                        community=community,
                        created_on=timezone.now(),
                        applicant=request.user,
                    )
                    new_application.save()
            else:
                create_membership(request.user)

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/home/'))

    else:
        form = UserPermissionForm()


    return render(request, 'community.html', {
        'mod_communities': mod_communities,
        'earner_communities': earner_communities,
        'username': request.user.username,
        'all_members' : all_memberships,
        'is_member' : membership.count()==1,
        'is_moderator' : moderator.count()==1,
        'community': community,
        'applied': application,
        'applications': all_applications,
        'UPForm' : form,
        'extendTemplate': extendTemplate
    })
