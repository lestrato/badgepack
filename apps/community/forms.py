from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class UserPermissionForm(forms.Form):
    CHOICES= (
    (False, 'earner'),
    (True, 'moderator'),
    )
    permissions = forms.CharField(
        widget=forms.Select(
            choices=CHOICES,
            attrs={
                "class":"form-control",
            }
        )
    )

class UserSearchForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'required':'True',
                'id':"user-name",
                'placeholder':"Add user...",
                'autocomplete':"off",
                "class":"form-control",
            }
        )
    )

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
            return self.cleaned_data['username']
        except User.DoesNotExist:
            raise forms.ValidationError(_("The username does not exist. Please try another one."))

class CommunityPrivacyForm(forms.Form):
    CHOICES= (
    (True, 'True'),
    (False, 'False'),
    )
    privacy = forms.CharField(
        widget=forms.Select(
            choices=CHOICES,
            attrs={
                "id":"privacyEditor",
                "style":"display: none;",
                "class":"form-control input-sm",
                }
        )
    )


class CommunityDescriptionForm(forms.Form):
    description = forms.CharField(
        widget=forms.Textarea(
            # for some reason, adding classes in the state attrs=dict() runs back a syntax error
            attrs={
                "id":"descriptionEditor",
                "style":"display: none; resize: vertical; ",
                "class":"form-control",
                }
        )
    )

    def clean_description(self):
        description = self.cleaned_data.get("description")
        return description
