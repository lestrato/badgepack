"""work URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from account.views import *
from community.views import *
from base.views import *

from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers
from api import views as api_views
from rest_framework.authtoken import views as authtoken_views

# router = routers.DefaultRouter()
# router.register(r'api/users', api_views.UserViewSet)
# router.register(r'api/communities', api_views.CommunityViewSet)

urlpatterns = [
    url(r'^$', login_page),
    url(r'^logout/$', logout_page),
    url(r'^accounts/login/$', login_page), # If user is not login it will redirect to login page
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^home/$', HomeView.as_view()),
    url(r'^community/(?P<community_tag>[a-z||A-Z||0-9]+)$', CommunityView.as_view(), name='community'),
    url(r'^search/$', SearchView.as_view()),
    url(r'^profile/(?P<profile_id>[a-z||A-Z||0-9||\-]+)$', ProfileView.as_view()),
    url(r'^profile/$', profile_page),
]

# API:
urlpatterns += [
    url(r'^', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/communities/(?P<community_tag>[a-z||A-Z||0-9]+)$', api_views.APICommunityView.as_view()),
    url(r'^api/communities/(?P<community_tag>[a-z||A-Z||0-9]+)/users$', api_views.APICommunityUsersView.as_view()),
    url(r'^api/communities/(?P<community_tag>[a-z||A-Z||0-9]+)/badges/(?P<user_id>[a-z||A-Z||0-9]+)$', 
        api_views.APISingleUserBadgeView.as_view()),
    url(r'^api/communities/(?P<community_tag>[a-z||A-Z||0-9]+)/badges$', api_views.APICommunityBadgesView.as_view()),
    url(r'^api/communities/(?P<community_tag>[a-z||A-Z||0-9]+)/leaderboard$', api_views.APILeaderboardView.as_view()),
    url(r'^api/replace-token/', api_views.APIReplaceTokenView.as_view()),
    url(r'^api/auth-token/', authtoken_views.obtain_auth_token),
    url(r'^api/$', api_views.api_root),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
