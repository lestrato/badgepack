from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.views import login
from django.utils.decorators import method_decorator

from account.fetches import *
from account.forms import *
from community.models import Invitation
from community.fetches import *
from badge.models import BadgeClass, BadgeInstance
from base.forms import *
from base.views import AbstractBaseView

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

@method_decorator(login_required, name='dispatch')
class HomeView(AbstractBaseView):
    template_name = 'home.html'

    def fetch(self, request):
        # fetch user's community invitations
        invitations = Invitation.objects.filter(
            recipient=request.user,
        )
        user_communities = Community.objects.filter(
            members=request.user,
        )

        self.template_items['invitations'] = invitations
        self.template_items['user_communities'] = user_communities
