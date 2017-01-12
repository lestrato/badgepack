from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.contrib.auth.views import login
from django.views import View

from base.forms import *
from community.models import Community
from account.fetches import *
from community.fetches import *

class AbstractBaseView(View):
    # these gets replaced by the parent class
    template_name = None
    template_items = {}
    community_tag = None

    def get(self, request, **kwargs):
        # fetch potential community tag
        self.community_tag = kwargs.get('community_tag', None)
        self.url_profile_id = kwargs.get('profile_id', None)

        # navbar information
        owner_communities = u_communities(
            members=request.user,
            user_status='owner',
        )
        mod_communities = u_communities(
            members=request.user,
            user_status='moderator',
        )
        earner_communities = u_communities(
            members=request.user,
            user_status='earner',
        )

        # forms
        searchform = CommunitySearchForm()

        # gather the above plus request.user into a dict to pass into the templ.
        self.template_items['owner_communities'] = owner_communities
        self.template_items['mod_communities'] = mod_communities
        self.template_items['earner_communities'] = earner_communities
        self.template_items['searchform'] = searchform
        self.template_items['user'] = request.user

        self.fetch(request)

        return render(request, self.template_name, self.template_items)

@method_decorator(login_required, name='dispatch')
class SearchView(AbstractBaseView):
    template_name = 'base/search.html'

    def fetch(self, request):
        if 'community' in request.GET:
            CSForm = CommunitySearchForm(request.GET)
            if CSForm.is_valid():
                search_input = CSForm.cleaned_data['community']
                # fetch search results
                all_results = Community.objects.filter(
                    name__icontains=search_input,
                )| Community.objects.filter(
                    tag__icontains=search_input,
                )| Community.objects.filter(
                    description__icontains=search_input,
                )

                self.template_items['search_input'] = search_input
                self.template_items['all_results'] = all_results
