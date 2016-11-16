from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render
from django.contrib.auth.views import login


from base.forms import *
from community.models import Community
from login.fetches import *

def search(request):
    search_input = None
    all_results = None
    if request.method == 'GET':
        print request.GET

        if 'community' in request.GET:
            CSForm = CommunitySearchForm(request.GET)
            if CSForm.is_valid():
                search_input = CSForm.cleaned_data['community']
                all_results = Community.objects.filter(
                    name__icontains=search_input,
                )| Community.objects.filter(
                    tag__icontains=search_input,
                )| Community.objects.filter(
                    description__icontains=search_input,
                )

    mod_communities, earner_communities = get_navbar_information(
        request=request,
    )
    searchform = CommunitySearchForm()

    return render(request, 'search.html', {
        'mod_communities': mod_communities,
        'earner_communities': earner_communities,
        'searchform': searchform,

        'search_input': search_input,
        'all_results': all_results,
    })
