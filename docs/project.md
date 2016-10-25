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


# Static Files (CSS)

    login/static/
        bootstrap/  # Bootstrap CSS and JS files.
        style.css   # Custom CSS (overrides Bootstrap CSS).

Badgepack makes use of Bootstrap CSS/JS as its base, with some of its style being overridden by `style.css`. This section details the contents of `style.css`.

Selector | Description/Notes
--- | ---
`body` | Main body of the pages |
`hr` | Horizontal rule; colour has been modified
`.navbar-default` | Navigation bar
`.navbar-default .navbar-nav > li > a` | Buttons / links in the navigation bar
`.badge-list` | Badge list; not included in Bootstrap
`.badge-list > li` | Members (badges) of the badge list; set to display like a 2- or 3-column table
`.badge-container` | Container for badges; width and height are set here
`.badge-image-container` | Container for the badge image; set to be aligned to the top
`.badge-image` | Contents of `.badge-image-container`; default: an empty 100x100 grey box
`.badge-image > img` | Resizes badges to fit the image container
`.badge-name` | Name/title of the badge
`.badge-description` | Contents of the badge
`.badge-footer` | Bottom row of the badge container; text of the bottom row is handled by `.badge-footer-left` and `.badge-footer-right`
`.badge-footer-left` | Left-most text of the badge footer (i.e. date created/earned)
`.badge-footer-right` | Right-most text of the badge footer (i.e. progress %)


# Login

Path: `/badgepack/login/`

## Templates

Name | Description
--- | ---
`home.html` | Homepage of the project; displayed when user is logged in
`nav.html` | Navigation bar of the project
`badge.html` | A single badge (recommended to exist within a badge list; refer to `badge_list_sample.html` for sample usage)
`badge_list_sample.html` | Sample implementation of a badge list
`registration/` | Directory containing templates related to login and registration
`registration/login.html` | Login page; leads to the homepage upon successful login
`registration/register.html` | Registration page
`registration/success.html` | Page served when a user has successfully registered

## Apps

## Forms

## Shared Views

## Views

# Community

Path: `/badgepack/community/`

## Templates

Name | Description
--- | ---
`community.html` | Base template for all community pages
`earner.html` | Community page as-seen by regular (non-moderator) members
`moderator.html` | Community page as-seen by community moderators
`visitor.html` | Community page as-seen by non-members of the community

## Admin

## Forms

## Models

## Views

