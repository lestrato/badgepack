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

    mod_communities, earner_communities = get_navbar_information(request)

    return render_to_response('home.html', {
    'invitations': invitations,
    'mod_communities': mod_communities,
    'earner_communities': earner_communities,
    'user': request.user,
    # 'badge_instances': badge_instances,
    })
