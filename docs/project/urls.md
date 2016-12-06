# URLs
    work
    ├── work

URL | View | Path
--- | --- | ---
`$`   | `login_page` | `apps/account/views.py`
`logout/$` | `logout_page` | `apps/account/views.py`
`accounts/login/$` | `login_page` | `apps/account/views.py`
`admin/` | `admin.site.urls` | `django.contrib`
`register/$` | `register` | `apps/account/views.py`
`register/success/$` | `register_success` | `apps/account/views.py`
`home/$` | `HomeView.as_view()` | `apps/account/views.py`
`community/($P<community_tag>[a-z||A-Z||0-9]+)$` | `CommunityView.as_view()` | `apps/community/views.py`
`search/$` | `SearchView.as_view()` |  `apps/base/views.py`
