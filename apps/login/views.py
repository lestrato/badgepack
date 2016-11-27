from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render
from django.contrib.auth.views import login

from login.fetches import *
from login.forms import *
from community.models import Invitation
from badge.models import BadgeClass, BadgeInstance
from base.forms import *

from community.views import *

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
        return render(request, 'login/login.html', {'form': form })

@csrf_protect
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

    return render(request, 'login/register.html', {'form': form})

def register_success(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    else:
        return render_to_response(
        'login/success.html',
        )

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def home(request):
    invitations = u_all_invitations(request.user)
    mod_communities, earner_communities = get_navbar_information(
        request=request,
    )
    searchform = CommunitySearchForm()
    pending_invites = u_pending_invitations(request.user)

    if request.method == 'POST':
        if "acceptPendingInviteBtn" in request.POST:
            # Get community based off tag:
            community = community_object(request.POST['acceptPendingInviteBtn'])

            # Check if user is a member of the community already:
            membership = u_membership(
                community=community,
                user=request.user,
            )

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

    return render(request, 'home.html', {
        'mod_communities': mod_communities,
        'earner_communities': earner_communities,
        'searchform': searchform,

        'user': request.user,
        'invitations': invitations,
        'pending_invitations': pending_invites,
    })