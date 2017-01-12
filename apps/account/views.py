from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render
from django.contrib.auth.views import login

from account.fetches import *
from account.forms import *
from community.models import Invitation
from community.fetches import *
from community.views import *
from badge.models import BadgeClass, BadgeInstance
from base.forms import *

def login_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    else:
        # return login(request, 'registration/login.html', MyAuthenticationForm)
        if request.method == 'POST':
            form = MyAuthenticationForm(request.POST)
            if form.is_valid():
                user = form.login(request)
                if user:
                    login(request, user)
                    return HttpResponseRedirect('/home/')
        else:
            form = MyAuthenticationForm()
        return render(request, 'account/login.html', {'form': form })

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'],
                    email=form.cleaned_data['email']
                )
                return HttpResponseRedirect('/register/success/')
        else:
            form = RegistrationForm()

    return render(request, 'account/register.html', {'form': form})

def register_success(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    else:
        return render_to_response(
        'account/success.html',
        )

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

@method_decorator(login_required, name='dispatch')
class HomeView(AbstractBaseView):
    template_name = 'base/home.html'

    def fetch(self, request):
        # fetch user's community invitations
        invitations = u_pending_invitations(request.user)
        user_communities = u_communities(request.user)

        self.template_items['invitations'] = invitations
        self.template_items['user_communities'] = user_communities

    def post(self, request, **kwargs):
        print request.POST

        if "acceptPendingInviteBtn" in request.POST:
            # Get community based off tag:
            community = community_object(request.POST['acceptPendingInviteBtn'])

            ''' User membership privilege refetching '''
            membership = u_membership(
                community=community,
                user=request.user,
            )

            if community:
                if not membership:
                    # Make sure user received an invitation:
                    invitation = u_invitation(
                                    community=community,
                                    user=request.user,
                                )
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

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/home/'))

def profile_page(request):
    profile = u_profile_by_user(user=request.user)

    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/{0}'.format(profile.profile_id))
    else:
        return render_to_response(
        'account/login.html',
        )


def check_user_authorization(request):
    return False

@method_decorator(login_required, name='dispatch')
class ProfileView(AbstractBaseView):
    template_name = 'account/profile.html'

    def fetch(self, request):
        print(self.url_profile_id)
        # Grab the profile:
        profile = u_profile(profile_id=self.url_profile_id)
        public_id = profile.public_id

        # Whether or not requester owns the profile:
        is_own_profile = (profile.user == request.user)
        
        # Determine whether or not requester can see the user's private ID:
        is_authorized_to_view_id = (check_user_authorization(request) or is_own_profile)

        # User's badges:
        earned_badges = u_all_badges(profile.user)
        print(earned_badges)

        # Forms:
        IDForm = PublicIdForm()         # edit public ID

        self.template_items['profile'] = profile
        self.template_items['public_id'] = public_id
        self.template_items['private_id'] = profile.user.username
        self.template_items['is_own_profile'] = is_own_profile
        self.template_items['is_authorized_to_view_id'] = is_authorized_to_view_id
        self.template_items['IDForm'] = IDForm
        self.template_items['earned_badges'] = earned_badges

    def post(self, request, **kwargs):
        print request.POST

        profile = u_profile_by_user(user=request.user)

        if 'submitPublicId' in request.POST:
            IDForm = PublicIdForm(request.POST)
            if IDForm.is_valid():
                profile = profile.edit_public_id(
                    public_id=IDForm.cleaned_data['public_id'],
                )
                profile.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/home/'))

# @login_required
# def home(request):
#     invitations = u_all_invitations(request.user)
#     mod_communities, earner_communities = get_navbar_information(
#         request=request,
#     )
#     searchform = CommunitySearchForm()
#     pending_invites = u_pending_invitations(request.user)

#     if request.method == 'POST':
#         if "acceptPendingInviteBtn" in request.POST:
#             # Get community based off tag:
#             community = community_object(request.POST['acceptPendingInviteBtn'])

#             # Check if user is a member of the community already:
#             membership = u_membership(
#                 community=community,
#                 user=request.user,
#             )

#             if not membership:
#                 # Make sure user received an invitation:
#                 invitation = u_invitation(
#                                 community=community,
#                                 user=request.user,
#                             )
#                 if invitation:
#                     # create new membership
#                     new_membership = Membership(
#                         user=request.user,
#                         community=community,
#                         is_moderator=invitation.to_be_moderator,
#                     )
#                     new_membership.save()

#                 # check if user already submitted an application to this community
#                 application = u_application(
#                     community=community,
#                     user=request.user,
#                 )
#                 if application:
#                     # and check if the application hasn't been accepted yet
#                     if not application.accepted_by:
#                         # cancel application
#                         application.delete()
#                 # if neither, create new application
#                 else:
#                     new_application = Application(
#                         applicant=request.user,
#                         community=community,
#                     )
#                     new_application.save()

#     return render(request, 'home.html', {
#         'mod_communities': mod_communities,
#         'earner_communities': earner_communities,
#         'searchform': searchform,

#         'user': request.user,
#         'invitations': invitations,
#         'pending_invitations': pending_invites,
#     })