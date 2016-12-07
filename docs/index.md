# Badgepack

Badgepack is a community-driven badge distribution reward system.

## Full Project Directory Layout
    work        # base folder; manage.py, readme, license
    ├── apps        # user-created applications
    │   ├── account     # registration, login, logout, home
    │   ├── badge       # badge class and instance
    │   ├── base        # abstract base class and search
    │   ├── community   # community, membership, invitation, application
    ├── docs        # documentation
    │   ├── guides      # to edit and create read-the-doc files
    │   ├── project     # the various project files
    │   ├── status      # administrative project information
    ├── media       # non-static media
    │   ├── uploads     # user-uploaded items
    │   │   ├── badges      # user-uploaded badges
    ├── static      # static files, fonts, stylings
    │   ├── bootstrap       
    │   |   ├── css         # bootstrap stylesheets
    │   |   ├── fonts       # bootstrap fonts
    │   |   ├── js          # bootstrap scripts
    │   ├── images      # static images
    │   ├── templates   # static viewable templates
    │   |   ├── account     # for the account 'app'
    │   |   ├── badge       # for the account 'badge'
    │   |   ├── base        # for the account 'base'
    │   |   ├── community   # for the account 'community'
    │   |   |   ├── components  # inheritable community pieces
    ├── work        # settings, urls
