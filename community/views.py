from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.html import escape

from community.models import Community, Membership, Application, Invitation
from community.forms import *
from login.sharedviews import get_navbar_information
from community.validators import validateUsername

@login_required
def community(request, community_tag):

    def accept_application(applicant, accepted_by):
        accepted_application = get_object_or_404(
            all_applications,
            applicant=applicant
        )

        accepted_application.accepted_by=accepted_by
        accepted_application.save()

        create_membership(accepted_application.applicant, False)

    # create membership based on whether the user created it for someone
    # else or for him/herself
    def create_membership(user_type, permissions):
        new_membership = Membership(
            user=user_type,
            community=community,
            joined_on=timezone.now(),
            is_moderator=permissions
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

    # all community invitations
    all_invitations = Invitation.objects.filter(
        community=community.id
    )

    # my community invitation
    invitation = Invitation.objects.filter(
        community=community.id,
        recipient=request.user.id,
    ).first()

    # fetch proper template extension based on current permissions
    if moderator:
        extendTemplate = 'moderator.html'
    elif membership:
        extendTemplate = 'earner.html'
    else:
        extendTemplate = 'visitor.html'

    UPForm = UserPermissionForm(request.POST or None)
    USForm = UserSearchForm(request.POST or None)
    CDForm = CommunityDescriptionForm(request.POST or None)
    CPForm = CommunityPrivacyForm(request.POST or None)

    if request.method == 'POST':

        print request.POST # TODO:for debugging

        if 'inviteSubmit' in request.POST:
            allInvites = request.POST.getlist('addedUser')

            # Sanitize and validate hidden invite input
            for invite in allInvites:
                username = escape(invite)

                if validateUsername(username):
                    # fetch user instance
                    invited_user = get_object_or_404(
                        User,
                        username=username
                    )

                    user_invite = all_applications.filter(
                        applicant=invited_user.id,
                    )

                    # check if user has a pending application
                    if user_invite.count() == 1:
                        # accept application and create membership
                        accept_application(invited_user, request.user)

                    else:
                        # create new invitation
                        new_invitation = Invitation(
                            community=community,
                            created_on=timezone.now(),
                            recipient=invited_user,
                            sender=request.user,
                        )
                        new_invitation.save()

        if 'permissionSubmit' in request.POST:
            UPForm = UserPermissionForm(request.POST)
            if UPForm.is_valid():
                user_membership = get_object_or_404(
                    all_memberships,
                    user=request.POST['member']
                )
                user_membership.is_moderator=UPForm.cleaned_data['permissions']
                user_membership.save()

        if 'inviteUsersSubmit' in request.POST:
            USForm = UserSearchForm(request.POST)
            if USForm.is_valid():
                # check if user is already in community
                is_member = Membership.objects.filter(
                    community_id=community.id,
                    user__username=request.POST['username'],
                )
                if is_member.count()==1:
                    error_message = 'You cannot add a user already in the community.'
                    SameUsernameError = {'username': error_message}
                    return JsonResponse(SameUsernameError)

                # check if invite already exists for user
                has_invitation = Invitation.objects.filter(
                    community_id=community.id,
                    recipient__username=request.POST['username'],
                )
                if has_invitation.count()==1:
                    error_message = 'An invite already exists for this user.'
                    InviteExistsError = {'username': error_message}
                    return JsonResponse(InviteExistsError)

                else:
                    return HttpResponse(request.POST['username'])
            else:
                # print USForm.errors
                return JsonResponse(USForm.errors)

        if 'acceptApplication' in request.POST:
            accept_application(request.POST['acceptApplication'], request.user)

        if 'communityJoin' in request.POST:
            # refetch community
            community = get_object_or_404(
                Community,
                tag=community_tag
            )
            # check if community is private or not
            if community.is_private:

                # refetch (potential) invitation
                invitation = Invitation.objects.filter(
                    community=community.id,
                    recipient=request.user.id,
                ).first()

                # check if user has been invited to this community
                if invitation:
                    create_membership(request.user, invitation.to_be_moderator)

                # check if user already submitted an application to this community
                if application:
                    # fetch application again
                    application = get_object_or_404(
                        Application,
                        community=community.id,
                        applicant=request.user.id
                    )
                    # and check if the application hasn't been accepted yet
                    if not application.accepted_by:
                        # cancel application
                        application.delete()

                # if neither, create new application
                else:
                    new_application = Application(
                        community=community,
                        created_on=timezone.now(),
                        applicant=request.user,
                    )
                    new_application.save()
            else:
                # if not private community, create membership
                create_membership(request.user, False)

        if 'revokeInvite' in request.POST:
            # get user's invite
            revoked_invite = get_object_or_404(
                all_invitations,
                recipient=request.POST['revokeInvite'],
            )
            revoked_invite.delete()

        if 'submitDescription' in request.POST:
            CDForm = CommunityDescriptionForm(request.POST)
            if CDForm.is_valid():
                # refetch community
                community = get_object_or_404(
                    Community,
                    tag=community_tag
                )
                # change the community description on backend
                community.description = request.POST['description']
                community.save()

        if 'changePrivacySubmit' in request.POST:
            CPForm = CommunityPrivacyForm(request.POST)
            if CPForm.is_valid():
                # refetch community
                community = get_object_or_404(
                    Community,
                    tag=community_tag
                )
                if request.POST['privacy'] == 'True':
                    # set privacy as true
                    community.is_private = True
                    community.save()

                elif request.POST['privacy'] == 'False':
                    # set applications to accepted
                    all_applications = Application.objects.filter(
                        community=community.id,
                    )
                    for application in all_applications.all():
                        # check if the application hasn't been accepted yet
                        if not application.accepted_by:
                            application.accepted_by = request.user
                            application.save()
                            create_membership(application.applicant, False)

                    # set privacy as false
                    community.is_private = False
                    community.save()
                    print 'done'


                # user_membership.is_moderator=UPForm.cleaned_data['permissions']
                # user_membership.save()

        if 'invitedPermissionSubmit' in request.POST:
            UPForm = UserPermissionForm(request.POST)
            if UPForm.is_valid():
                # refetch invitation
                user_invite = get_object_or_404(
                    Invitation,
                    recipient=request.POST['invited']
                )
                user_invite.to_be_moderator=UPForm.cleaned_data['permissions']
                user_invite.save()

        # in all the above cases, return to same page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/home/'))

    else:
        UPForm = UserPermissionForm()
        USForm = UserSearchForm()
        CDForm = CommunityDescriptionForm()
        CPForm = CommunityPrivacyForm()

    return render(request, 'community.html', {
        'mod_communities': mod_communities,
        'earner_communities': earner_communities,

        'username': request.user.username,

        'all_invitations': all_invitations,
        'is_invited': invitation != None,

        'all_members' : all_memberships,
        'is_member' : membership.count()==1,

        'is_moderator' : moderator.count()==1,

        'community': community,

        'has_applied': application,
        'applications': all_applications,

        'UPForm' : UPForm,
        'USForm' : USForm,
        'CDForm' : CDForm,
        'CPForm' : CPForm,

        'extendTemplate': extendTemplate
    })
