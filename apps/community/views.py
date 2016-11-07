from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.utils import timezone
from django.utils.html import escape
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.forms.formsets import formset_factory

from community.forms import *
from community.models import *
from community.validators import validateUsername
from community.fetches import *

from badge.fetches import *
from badge.forms import *

from login.fetches import *


@login_required
def community(request, community_tag):
    ''' FETCH INFORMATION '''
    # get information for navbar
    mod_communities, earner_communities = get_navbar_information(
        request=request,
    )
    # this commounity, based on tag
    community = community_object(
        community_tag=community_tag,
    )
    # user's membership
    membership = u_membership(
        community=community,
        user=request.user,
    )
    # all community memberships
    all_memberships = all_community_memberships(
        community=community,
    )
    # user's applications
    application = u_application(
        community=community,
        user=request.user,
    )
    # all community applications
    all_applications = all_community_applications(
        community=community,
    )
    # user's invitation
    invitation = u_invitation(
        community=community,
        user=request.user,
    )
    # all community invitations
    all_invitations = all_community_invitations(
        community=community,
    )
    # all community badge classes
    all_badges = all_community_badge_classes(
        community=community
    )

    # use proper template extension based on current permissions
    if not membership:
        is_moderator = False
        extendTemplate = 'community/visitor.html'
    elif membership.is_moderator:
        is_moderator = True
        extendTemplate = 'community/moderator.html'
    else:
        is_moderator = False
        extendTemplate = 'community/earner.html'


    ''' FORMSET CREATION '''
    UBAFormset = formset_factory(
        UserBadgeAssignForm,
        extra=all_badges.count(),
    )
    OBAFormset = formset_factory(
        OneBadgeAssignForm,
        extra=all_memberships.count(),
    )

    if request.method == 'POST':
        print request.POST # TODO:for debugging
        # we ALWAYS refetch community
        community = community_object(community_tag)
        # we ALWAYS refetch membership status
        membership = u_membership(
            community=community,
            user=request.user,
        )

        if community:
            if not membership:
                # if user is not a member
                if 'communityJoin' in request.POST:
                    # check if community is private or not
                    if community and community.is_private:
                        # refetch (potential) invitation
                        invitation = u_invitation(
                            community=community,
                            user=request.user,
                        )
                        # check if user has been invited to this community
                        if invitation:
                            # create new membership
                            new_membership = Membership(
                                user=request.user,
                                community=community,
                                is_moderator=invitation.to_be_moderator,
                            )
                            new_membership.save()
                        # check if user already submitted an application to this community
                        application = u_application(
                            community=community,
                            user=request.user,
                        )
                        if application:
                            # and check if the application hasn't been accepted yet
                            if not application.accepted_by:
                                # cancel application
                                application.delete()
                        # if neither, create new application
                        else:
                            new_application = Application(
                                applicant=request.user,
                                community=community,
                            )
                            new_application.save()
                    else:
                        # if not private community, create membership
                        new_membership = Membership(
                            user=request.user,
                            community=community,
                            is_moderator=False,
                        )
                        new_membership.save()

            elif membership.is_moderator:
                # otherwise, if user is a moderator and community still exists
                ''' Community invitations and applications
                '''
                if 'inviteSubmit' in request.POST:
                    allInvites = request.POST.getlist('addedUser')
                    # Sanitize and validate hidden invite input
                    for invite in allInvites:
                        username = escape(invite)
                        if validateUsername(username):
                            # fetch user instance
                            invited_user = u_instance(
                                username=username,
                            )
                            if invited_user:
                                # check if user has a pending application
                                application = u_application(
                                    community=community,
                                    user=invited_user,
                                )
                                if application:
                                    # accept application and create membership
                                    application = application.accept(
                                        accepted_by=request.user,
                                    )
                                    application.save()
                                    # create new membership
                                    new_membership = Membership(
                                        user=invited_user,
                                        community=community,
                                        is_moderator=False,
                                    )
                                    new_membership.save()

                                else:
                                    # create new invitation
                                    new_invitation = Invitation(
                                        community=community,
                                        recipient=invited_user,
                                        sender=request.user,
                                    )
                                    new_invitation.save()

                if 'inviteUserSubmit' in request.POST:
                    USForm = UserSearchForm(request.POST)
                    if USForm.is_valid():
                        # get user instance
                        user = u_instance(request.POST['username'])
                        # form already checks if user exists, so no need to check again
                        # check if user is already in community
                        membership = u_membership(
                            community=community,
                            user=user,
                        )
                        if membership:
                            error_message = 'You cannot add a user already in the community.'
                            SameUsernameError = {'username': error_message}
                            return JsonResponse(SameUsernameError)
                        # check if invite already exists for user
                        invitation = u_invitation(
                            community=community,
                            user=user,
                        )
                        if invitation:
                            error_message = 'An invite already exists for this user.'
                            InviteExistsError = {'username': error_message}
                            return JsonResponse(InviteExistsError)
                        else:
                            return HttpResponse(request.POST['username'])
                    else:
                        # print USForm.errors
                        return JsonResponse(USForm.errors)

                if 'acceptApplication' in request.POST:
                    # check if user has a pending application
                    application = u_application(
                        community=community,
                        user=request.POST['acceptApplication'],
                    )
                    if application:
                        # accept application and create membership
                        application = application.accept(
                            accepted_by=request.user,
                        )
                        application.save()

                if 'revokeInvite' in request.POST:
                    # fetch user's instance
                    user = u_instance(request.POST['revokeInvite'])
                    if user:
                        # get user's invite
                        invite = u_invitation(
                            community=community,
                            user=user,
                        )
                        if invite:
                            invite.delete()

                if 'invitedPermissionSubmit' in request.POST:
                    UPForm = UserPermissionForm(request.POST)
                    if UPForm.is_valid():
                        # refetch invitation
                        invite = u_invitation(
                            community=community,
                            user=request.POST['invited'],
                        )
                        if invite:
                            invite = invite.edit_permissions(
                                permissions=UPForm.cleaned_data['permissions'],
                            )
                            invite.save()


                ''' User permissions and membership
                '''
                if 'permissionSubmit' in request.POST:
                    UPForm = UserPermissionForm(request.POST)
                    if UPForm.is_valid():
                        # get user membership and check if it exists
                        membership = u_membership(
                            community=community,
                            user=request.POST['member']
                        )

                        if membership:
                            # change permission
                            membership = membership.edit_permissions(
                                permissions=UPForm.cleaned_data['permissions'],
                            )
                            membership.save()

                if 'communityJoin' in request.POST:
                    # check if community is private or not
                    if community and community.is_private:
                        # refetch (potential) invitation
                        invitation = u_invitation(
                            community=community,
                            user=request.user,
                        )
                        # check if user has been invited to this community
                        if invitation:
                            # create new membership
                            new_membership = Membership(
                                user=request.user,
                                community=community,
                                is_moderator=invitation.to_be_moderator,
                            )
                            new_membership.save()
                        # check if user already submitted an application to this community
                        application = u_application(
                            community=community,
                            user=request.user,
                        )
                        if application:
                            # and check if the application hasn't been accepted yet
                            if not application.accepted_by:
                                # cancel application
                                application.delete()
                        # if neither, create new application
                        else:
                            new_application = Application(
                                applicant=request.user,
                                community=community,
                            )
                            new_application.save()
                    else:
                        # if not private community, create membership
                        new_membership = Membership(
                            user=request.user,
                            community=community,
                            is_moderator=False,
                        )
                        new_membership.save()


                ''' Community settings
                '''
                if 'submitDescription' in request.POST:
                    CDForm = CommunityDescriptionForm(request.POST)
                    if CDForm.is_valid():
                        # change the community description on backend
                        community = community.edit_description(
                            description=request.POST['description'],
                        )
                        community.save()

                if 'changePrivacySubmit' in request.POST:
                    CPForm = CommunityPrivacyForm(request.POST)
                    if CPForm.is_valid():
                        if request.POST['privacy'] == 'True':
                            # set privacy as true
                            community = community.change_privacy(
                                change_privacy=True,
                            )
                            community.save()
                        elif request.POST['privacy'] == 'False':
                            # set applications to accepted
                            all_applications = all_community_applications(
                                community=community,
                            )
                            for application in all_applications.all():
                                # check if the application hasn't been accepted yet
                                if not application.accepted_by:
                                    application = application.accept(
                                        accepted_by=request.user,
                                    )
                                    application.save()
                                    # create new membership
                                    new_membership = Membership(
                                        user=request.user,
                                        community=community,
                                        is_moderator=False,
                                    )
                                    new_membership.save()
                            # set privacy as false
                            community = community.change_privacy(
                                is_private=False
                            )
                            community.save()


                ''' Badges
                '''
                if 'addBadgeSubmit' in request.POST:
                    BCForm = BadgeCreationForm(request.POST, request.FILES)
                    if BCForm.is_valid():
                        # create new badgeclass
                        new_badgeclass = BadgeClass(
                            name=request.POST['name'],
                            description=request.POST['description'],
                            image=request.FILES['image'],
                            community=community,
                            creator=request.user,
                        )
                        new_badgeclass.save()

                if 'assignBadgesSubmit' in request.POST:
                    uba_formset = UBAFormset(request.POST)
                    if uba_formset.is_valid():
                        # fetch community membership
                        membership = u_membership(
                            user=request.POST['assignBadgesSubmit'],
                        )
                        if not membership:
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/home/'))

                        # refetch community badge classes
                        all_badges = all_badges_classes(
                            community=community,
                        )
                        # TODO: there should be a better way to couple the form number and the
                        #       badge class it represents
                        form_counter = 0
                        for badgeclass in all_badges:
                            # check if badgeclass exists in community
                            if badgeclass in all_badge_classes(community=community) and uba_formset[form_counter].cleaned_data.get('badge_assign') == 'gift':
                                # check if badgeinstance exists for the user
                                badgeinstance = u_badge_instance(
                                    badgeclass=badgeclass,
                                    earner=membership,
                                )
                                if not badgeinstance:
                                    # create new badge instance
                                    new_badgeinstance = BadgeInstance(
                                        badge_class=badgeclass,
                                        earner=membership.user,
                                        assigned_by=request.user,
                                    )
                                    new_badgeinstance.save()
                            form_counter += 1

                if 'oneBadgeSubmit' in request.POST:
                    oba_formset = OBAFormset(request.POST)
                    if oba_formset.is_valid():
                        # refetch all memberships
                        all_memberships = all_community_memberships(
                            community=community,
                        )
                        # fetch badge class
                        badge_class = a_badge_class(
                            class_name=request.POST['oneBadgeSubmit'],
                        )
                        # check if badge class exists and is part of the community
                        if badge_class and badge_class in all_badge_classes(community=community):
                            # TODO: there should be a better way to couple the form number and the
                            #       membership it represents
                            form_counter = 0
                            for member in all_memberships:
                                if oba_formset[form_counter].cleaned_data.get('badge_assign'):
                                    # check if user is in the community
                                    if not u_membership(community, member.user):
                                        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/home/'))

                                    # check if badgeinstance exists for the user
                                    badgeinstance = u_badge_instance(
                                        badgeclass=badge_class,
                                        earner=member.user,
                                    )
                                    if not badgeinstance:
                                        # create new badge instance
                                        new_badgeinstance = BadgeInstance(
                                            badge_class=badge_class,
                                            earner=member.user,
                                            assigned_by=request.user,
                                        )
                                        new_badgeinstance.save()
                                form_counter += 1

                if 'changeBadgeAvailabilitySubmit' in request.POST:
                    # fetch badge class
                    badge_class = a_badge_class(
                        class_name=escape(request.POST['changeBadgeAvailabilitySubmit']),
                    )
                    # check if badge_class is in this community
                    if badge_class and badge_class in all_badge_classes(community=community):
                        if badge_class.is_available:
                            badge_class.is_available = False
                        else:
                            badge_class.is_available = True
                        badge_class.save()

                if 'discontinueBadgeSubmit' in request.POST:
                    # fetch badge class
                    badge_class = a_badge_class(
                        class_name=escape(request.POST['discontinueBadgeSubmit']),
                    )
                    # check if badge_class is in this community
                    if badge_class and badge_class in all_badge_classes(community=community):
                        # destroy the badge
                        badge_class.delete()

        # in ALL the above cases, return to same page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/home/'))

    else:
        ''' FORM CREATION '''
        BCForm = BadgeCreationForm()
        UPForm = UserPermissionForm()
        USForm = UserSearchForm()
        CDForm = CommunityDescriptionForm()
        CPForm = CommunityPrivacyForm()
        BSAForm = BadgeSetAvailabilityForm()

    return render(request, 'community/community.html', {
        'mod_communities': mod_communities,
        'earner_communities': earner_communities,

        'user': request.user,
        'community': community,

        'all_members' : all_memberships,
        'is_member' : membership,
        'is_moderator' : is_moderator,

        'applications': all_applications,
        'has_applied': application,

        'all_invitations': all_invitations,
        'is_invited': invitation,

        'all_badge_classes' : all_badges,

        'BCForm' : BCForm,
        'UPForm' : UPForm,
        'USForm' : USForm,
        'CDForm' : CDForm,
        'CPForm' : CPForm,
        'BSAForm' : BSAForm,
        'UBAFormset' : UBAFormset,
        'OBAFormset' : OBAFormset,

        'extendTemplate': extendTemplate,
    })
