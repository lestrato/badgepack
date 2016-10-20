# Badgepack Server

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
* `source env/scripts/activate` *Activate the environment (each time you start a session working with the code)*

*Obtain source code and clone into code directory*

* `git clone https://github.com/concentricsky/badgr-server.git work`
* `cd work`

*Your Directory structure will look like this:*
```
badgepack
├── work
│   ├── build
│   ├── community
│   ├── login
│   ├── work
├── env
```

### Install requirements
*from within badgepack/work directory*

* `pip install mysql-python`
* `pip install django-widget-tweaks`

### Customize local settings to your environment and install database
* Edit the work/settings.py file and insert local credentials for DATABASES
* `mysql -u username -p database_name < badges.sql`

### Migrate databases, build front-end components
* `./manage.py migrate`
* `./manage.py createsuperuser` or `winpty ./manage.py createsuperuser` *follow prompts to create your first admin user account*

### Run a server locally for development
* `./manage.py runserver`
* Navigate to http://localhost:8000/
* Login with superuser or create new account

### Creating admins
* Navigate to http://localhost:8000/admin
* Login with superuser
* Select user to promote to admin
* Add to group: Admins
