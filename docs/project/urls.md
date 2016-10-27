# URLs

Path: `/badgepack/work/urls.py`

URL | View | Path
--- | --- | ---
`$`   | `login_page` | `login/views.py`
`logout/$` | `logout_page` | `login/views.py`
`accounts/login/$` | `login_page` | `login/views.py`
`admin/` | `admin.site.urls` | `django.contrib`
`register/$` | `register` | `login/views.py`
`register/success/$` | `register_success` | `login/views.py`
`home/$` | `home` | `login/views.py`
`community/($P<community_tag>[a-z||A-Z||0-9]+)$` | `community` | `community/views.py`