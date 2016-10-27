from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class UserPermissionForm(forms.Form):
    CHOICES= (
    (False, 'earner'),
    (True, 'moderator'),
    )
    permissions = forms.CharField(widget=forms.Select(choices=CHOICES))

class UserSearchForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs=dict(
                required=True,
                id="user-name",
                placeholder="Add user...",
                autocomplete="off",
            ),
        ),
    )

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
            return self.cleaned_data['username']
        except User.DoesNotExist:
            raise forms.ValidationError(_("The username does not exist. Please try another one."))
