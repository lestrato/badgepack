from django import forms
from django.contrib.auth.models import User

class UserPermissionForm(forms.Form):
    CHOICES= (
    (False, 'earner'),
    (True, 'moderator'),
    )
    permissions = forms.CharField(widget=forms.Select(choices=CHOICES))
