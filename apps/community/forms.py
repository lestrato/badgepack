from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class UserPermissionForm(forms.Form):
    CHOICES= (
    ('earner', 'earner'),
    ('moderator', 'moderator'),
    ('owner', 'owner'),
    )
    permissions = forms.CharField(
        widget=forms.Select(
            choices=CHOICES,
            attrs={
                "class":"form-control input-sm",
                'required':'True',
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
                "class":"form-control input-sm",
            }
        )
    )

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
            return self.cleaned_data['username']
        except User.DoesNotExist:
            raise forms.ValidationError(_("The username does not exist. Please try another one."))

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "required":True,
                "type":"file",
                "id":"csvUpload",
            }
        )
    )

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        file_name = csv_file.name
        if file_name.endswith('.csv'):
            if csv_file._size > 5242880:
                raise forms.ValidationError(_('Please keep filesize under 5mb. Current filesize %s') % (filesizeformat(csv_file._size)))
        else:
            raise forms.ValidationError(_('File type is not supported'))

        return csv_file

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
