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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
