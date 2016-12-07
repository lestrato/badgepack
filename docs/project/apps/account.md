# Backend
    work
    ├── apps
    │   ├── account

## admin.py
There doesn't seem to be anything here.

## fetches.py
Name | Description
--- | ---
`get_navbar_information(request)` | **Returns**: the communities the user is a moderator in, is an earner in
`get_search_form()` | **Returns**: the CommunitySearchForm
`u_instance(username)` | **Returns**: the user object associated with this username
`u_pending_invitations(user)` | **Returns**: all pending invitations for this user

## forms.py
Name | Description
--- | ---
`MyAuthenticationForm` | **Fields**: username, password<br>**Functions**: clean(self), login(self, request)
`RegistrationForm` | **Fields**: username, email, password1, password2<br>**Functions**: clean_username(self), def clean(self)

## models.py
There doesn't seem to be anything here.

## tests.py
There doesn't seem to be anything here.

## views.py
* `def login_page(request)`
* `def register(request)`
* `def register_success(request)`
* `def logout_page(request)`
* `class HomeView(AbstractBaseView)`

---
# Frontend

    work
    ├── static
    │   ├── templates
    │   |   ├── account

## templates
Name | Description
--- | ---
`login.html` | Login page; leads to the homepage upon successful login
`register.html` | Registration page
`success.html` |  Page served when a user has successfully registered
