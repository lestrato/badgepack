from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator

from community.forms import *
from community.models import *
from community.validators import validateUsername
from community.fetches import *

from badge.fetches import *
from badge.forms import *

from account.fetches import *

from base.views import AbstractBaseView

@method_decorator(login_required, name='dispatch')
class CommunityView(AbstractBaseView):
    template_name = 'community/community.html'

    def fetch(self, request):
        ''' FETCH INFORMATION '''
        # this commounity, based on tag
        community = community_object(
            community_tag=self.community_tag,
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
        all_badges = all_badge_classes(
            community=community
        )
        # all available community badge classes
        all_avail_badges = all_available_badge_classes(
            community=community,
        )

        # use proper template extension based on current permissions
        if not membership:
            user_status = 'visitor'
            extendTemplate = 'community/visitor.html'
        elif membership.user_status == 'owner':
            user_status = 'owner'
            extendTemplate = 'community/owner.html'
        elif membership.user_status == 'moderator':
            user_status = 'moderator'
            extendTemplate = 'community/moderator.html'
        else:
            user_status = 'earner'
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


        ''' FORM CREATION '''
        BCForm = BadgeCreationForm()
        UPForm = UserPermissionForm()
        USForm = UserSearchForm()
        CUForm = CSVUploadForm()
        CDForm = CommunityDescriptionForm()
        CPForm = CommunityPrivacyForm()
        BSAForm = BadgeSetAvailabilityForm()

        self.template_items['community'] = community
        self.template_items['all_members'] = all_memberships
        self.template_items['membership'] = membership
        self.template_items['user_status'] = user_status
        self.template_items['applications'] = all_applications
        self.template_items['has_applied'] = application
        self.template_items['all_invitations'] = all_invitations
        self.template_items['is_invited'] = invitation
        self.template_items['all_badge_classes'] = all_badges
        self.template_items['all_avail_badges'] = all_avail_badges
        self.template_items['BCForm'] = BCForm
        self.template_items['UPForm'] = UPForm
        self.template_items['USForm'] = USForm
        self.template_items['CUForm'] = CUForm
        self.template_items['CDForm'] = CDForm
        self.template_items['CPForm'] = CPForm
        self.template_items['BSAForm'] = BSAForm
        self.template_items['UBAFormset'] = UBAFormset
        self.template_items['OBAFormset'] = OBAFormset
        self.template_items['extendTemplate'] = extendTemplate

    def post(self, request, **kwargs):
        print request.POST

        ''' Community refetching '''
        self.community_tag = kwargs.get('community_tag', None)
        community = community_object(
            community_tag=self.community_tag,
        )

        ''' User membership privilege refetching '''
        membership = u_membership(
            community=community,
            user=request.user,
        )

        ''' FORMSET CREATION '''
        # all community memberships
        all_memberships = all_community_memberships(
            community=community,
        )
        # all community badge classes
        all_badges = all_badge_classes(
            community=community
        )
        UBAFormset = formset_factory(
            UserBadgeAssignForm,
            extra=all_badges.count(),
        )
        OBAFormset = formset_factory(
            OneBadgeAssignForm,
            extra=all_memberships.count(),
        )

        if community:
            if not membership:
                '''
                    Visitors can:
                    - apply to join the private community,
                    - join the public community,
                    - accept an invite to that community,
                '''
                if 'communityJoin' in request.POST:
                    # check if community is private or not
                    if community.is_private:
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
                                user_status='earner',
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
                            user_status='earner',
                        )
                        new_membership.save()

            elif membership.user_status == 'owner' or membership.user_status == 'moderator':
                '''
                    Moderators and owners can:
                    - assign badges,
                    - accept applications,
                    - create invitations,
                    - revoke invitations,
                '''

                ''' Community invitations and applications '''
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
                                        user_status='earner',
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

                if 'uploadCSVSubmit' in request.POST:
                    import json
                    CUForm = CSVUploadForm(request.POST, request.FILES)
                    if CUForm.is_valid():
                        print 'valid form'
                        data = CUForm.cleaned_data['csv_file']
                        csv_users = []
                        for line in CUForm.cleaned_data['csv_file']:
                            line = line.strip()
                            # check if user exists and get user instance
                            user = u_instance(
                                username=line
                            )
                            if user:
                                # check if user is already in community
                                membership = u_membership(
                                    community=community,
                                    user=user,
                                )
                                if not membership:
                                    # check if invite already exists for user
                                    invitation = u_invitation(
                                        community=community,
                                        user=user,
                                    )
                                    if not invitation:
                                        csv_users.append(line)

                        # print csv_users
                        return HttpResponse(json.dumps({'usernames': csv_users}))
                    else:
                        return JsonResponse(CUForm.errors)

                if 'inviteUserSubmit' in request.POST:
                    USForm = UserSearchForm(request.POST)
                    if USForm.is_valid():
                        # get user instance
                        user = u_instance(USForm.cleaned_data['username'])
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
                            return HttpResponse(USForm.cleaned_data['username'])
                    else:
                        # print USForm.errors
                        return JsonResponse(USForm.errors)

                if 'acceptApplication' in request.POST:
                    user = u_instance(request.POST['acceptApplication'])
                    # check if user has a pending application
                    application = u_application(
                        community=community,
                        user=user,
                    )
                    if application:
                        # accept application and create membership
                        application = application.accept(
                            accepted_by=request.user,
                        )
                        application.save()
                        # create new membership
                        new_membership = Membership(
                            user=user,
                            community=community,
                            user_status='earner',
                        )
                        new_membership.save()

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

                # TODO: More thoughts needs to be done about the below: should owners
                # be the only ones who can edit permissions before join-time?
                # if 'invitedPermissionSubmit' in request.POST:
                #     UPForm = UserPermissionForm(request.POST)
                #     if UPForm.is_valid():
                #         # fetch user's instance
                #         user = u_instance(request.POST['invited'])
                #         # refetch invitation
                #         invite = u_invitation(
                #             community=community,
                #             user=user,
                #         )
                #         if invite:
                #             invite = invite.edit_permissions(
                #                 permissions=UPForm.cleaned_data['permissions'],
                #             )
                #             invite.save()

                ''' Badges '''
                if 'assignBadgesSubmit' in request.POST and 'form-TOTAL_FORMS' in request.POST:
                    uba_formset = UBAFormset(request.POST)
                    if uba_formset.is_valid():
                        # fetch user instance
                        user = u_instance(request.POST['assignBadgesSubmit'])
                        # fetch community membership
                        membership = u_membership(
                            community=community,
                            user=user,
                        )
                        if membership:
                            # refetch available community badge classes
                            all_badges = all_available_badge_classes(
                                community=community,
                            )
                            # TODO: there should be a better way to couple the form number and the
                            #       badge class it represents
                            form_counter = 0
                            for badgeclass in all_badges:
                                # check if badgeclass exists in community and the badge is made available and if the moderator is gifting the badge
                                if badgeclass in all_badge_classes(community=community) and badgeclass.is_available and uba_formset[form_counter].cleaned_data['badge_assign'] == 'gift':
                                    # check if badgeinstance exists for the user
                                    badgeinstance = u_badge_instance(
                                        badgeclass=badgeclass,
                                        earner=user,
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
                            class_name=escape(request.POST['oneBadgeSubmit']),
                        )
                        # check if badge class exists and is part of the community and is available
                        if badge_class and badge_class.is_available and badge_class in all_badge_classes(community=community):
                            # TODO: there should be a better way to couple the form number and the
                            #       membership it represents
                            form_counter = 0
                            for member in all_memberships:
                                if oba_formset[form_counter].cleaned_data.get('badge_assign'):
                                    # check if user is in the community
                                    if u_membership(community, member.user):
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

                if membership.user_status == 'owner':
                    '''
                        Owners can also:
                        - change availability of a badge,
                        - edit a badge,
                        - discontinue a badge,
                        - change communtiy settings (description, privacy)
                        - change user permissions
                    '''

                    ''' User permissions and membership '''
                    if 'permissionSubmit' in request.POST:
                        UPForm = UserPermissionForm(request.POST)
                        if UPForm.is_valid():
                            # fetch user's instance
                            user = u_instance(request.POST['member'])
                            # get user membership and check if it exists
                            membership = u_membership(
                                community=community,
                                user=user,
                            )
                            if membership:
                                # change permission
                                membership = membership.edit_permissions(
                                    permissions=UPForm.cleaned_data['permissions'],
                                )
                                membership.save()


                    ''' Community settings '''
                    if 'submitDescription' in request.POST:
                        CDForm = CommunityDescriptionForm(request.POST)
                        if CDForm.is_valid():
                            # change the community description on backend
                            community = community.edit_description(
                                description=CDForm.cleaned_data['description'],
                            )
                            community.save()

                    if 'changePrivacySubmit' in request.POST:
                        CPForm = CommunityPrivacyForm(request.POST)
                        if CPForm.is_valid():
                            if CPForm.cleaned_data['privacy'] == 'True':
                                # set privacy as true
                                community = community.change_privacy(
                                    is_private=True,
                                )
                                community.save()
                            elif CPForm.cleaned_data['privacy'] == 'False':
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
                                            user_status='earner',
                                        )
                                        new_membership.save()
                                # set privacy as false
                                community = community.change_privacy(
                                    is_private=False
                                )
                                community.save()


                    ''' Badges '''
                    if 'addBadgeSubmit' in request.POST:
                        BCForm = BadgeCreationForm(request.POST, request.FILES)
                        if BCForm.is_valid():
                            # check if badgeclass name exists already
                            if not a_badge_class(BCForm.cleaned_data['name']):
                                # create new badgeclass
                                new_badgeclass = BadgeClass(
                                    name=BCForm.cleaned_data['name'],
                                    description=BCForm.cleaned_data['description'],
                                    image=BCForm.cleaned_data['image'],
                                    community=community,
                                    creator=request.user,
                                )
                                new_badgeclass.save()
                        else:
                            return JsonResponse(BCForm.errors)

                    if 'editBadgeSubmit' in request.POST:
                        BCForm = BadgeCreationForm(request.POST, request.FILES)
                        if BCForm.is_valid():
                            # fetch badge class
                            badge_class = a_badge_class(request.POST['editBadgeSubmit'])

                            # check if badge_class is in this community and if the badge is unavailable
                            if badge_class and not badge_class.is_available and \
                                badge_class in all_badge_classes(community=community):
                                # check if badgeclass is same as this one or name doesnt exist already
                                if BCForm.cleaned_data['name'] == request.POST['editBadgeSubmit'] or \
                                    not a_badge_class(BCForm.cleaned_data['name']):
                                    # change badge_class
                                    badge_class.name = BCForm.cleaned_data['name']
                                    badge_class.description = BCForm.cleaned_data['description']
                                    # remove old image from folder
                                    badge_class.image.delete()
                                    badge_class.image = BCForm.cleaned_data['image']
                                    badge_class.save()

                    if 'setBadgeAvailableSubmit' in request.POST:
                        # fetch badge class
                        badge_class = a_badge_class(
                            class_name=escape(request.POST['setBadgeAvailableSubmit']),
                        )
                        # check if badge_class is in this community
                        if badge_class and badge_class in all_badge_classes(community=community):
                            # set badge to unavailable
                            badge_class.is_available = True
                            badge_class.save()

                    if 'discontinueBadgeSubmit' in request.POST:
                        # fetch badge class
                        badge_class = a_badge_class(
                            class_name=escape(request.POST['discontinueBadgeSubmit']),
                        )
                        # check if badge_class is in this community
                        if badge_class and badge_class in all_badge_classes(community=community):
                            # remove old image from folder
                            badge_class.image.delete()
                            # destroy the badge
                            badge_class.delete()

        # in ALL the above cases, return to same page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/home/'))
