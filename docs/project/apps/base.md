# Backend
    work
    ├── apps
    │   ├── base

## admin.py
There doesn't seem to be anything here.

## fetches.py
There doesn't seem to be anything here.

## forms.py
Name | Description
--- | ---
`CommunitySearchForm` | **Fields**: community<br>**Functions**: none

## models.py
There doesn't seem to be anything here.

## tests.py
There doesn't seem to be anything here.

## views.py
* `class AbstractBaseView(View)`
* `class SearchView(AbstractBaseView)`

---
# Frontend

    work
    ├── static
    │   ├── templates
    │   |   ├── base

## templates
Name | Description
--- | ---
`base.html` | Inherited by every template in the system; includes styling, metadata, and static files
`home.html` | Homepage of the project; displayed when user is logged in
`nav.html` | Navigation bar of the project
`search.html` | Community-search results page
