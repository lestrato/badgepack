# Installation and Setup

*Version: 0.1*

## How to get started on your local development environment.
#### Prerequisites:

* git
* python 2.7.x
* virtualenv
* mysql

### Create project directory and environment

* `mkdir badgepack && cd badgepack`
* `virtualenv env`
* `source env/bin/activate` *Activate the environment (each time you start a session working with the code)*

*Obtain source code and clone into code directory*

* `git clone https://github.com/lestrato/badgepack.git work`
* `cd work`

*Your Directory structure will look like this:*
```
badgepack
├── work
│   ├── community
│   ├── login
│   ├── work
├── env
```

### Install requirements
From within `badgepack/work` directory:

* `pip install Django==1.10.2`
* `pip install mysql-python`
* `pip install django-widget-tweaks`

### Customize local settings to your environment
* `cp work/settings.py.example work/settings.py`
* Edit the work/settings.py file and insert local credentials for DATABASES

### Migrate databases, build front-end components
* `./manage.py migrate`
* `./manage.py createsuperuser` or `winpty python manage.py createsuperuser`
    * Follow the prompts to create your first admin user account

### Run a server locally for development
* `./manage.py runserver`
* Navigate to http://localhost:8000/
* Login with superuser or create new account

### Creating the admin group
* Navigate to http://localhost:8000/admin
* Login with superuser
* Navigate to http://localhost:8000/admin/auth/group/add/
* Set 'Name' as Admin
* Add privileges to Admin (recommended are add, change, delete for community and membership)
* Save

### Setting users as admins
* Navigate to http://localhost:3000/admin/auth/user/
* Select user to promote to admin
* Tick the 'Staff Status' checkbox under 'Permissions'
* Add to group 'Admin'
* Save