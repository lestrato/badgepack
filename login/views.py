from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render
from django.contrib.auth.views import login

from login.sharedviews import get_navbar_information
from login.forms import *

def login_page(request):
    if request.user.is_authenticated():
        return  HttpResponseRedirect('/home/')
    else:
        return login(request)

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

    return render(request, 'registration/register.html', {'form': form})

def register_success(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    else:
        return render_to_response(
        'registration/success.html',
        )

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def home(request):
    mod_communities, earner_communities = get_navbar_information(request)
    return render_to_response('home.html', {
    'mod_communities': mod_communities,
    'earner_communities': earner_communities,
    'username': request.user.username,
    })
