import re
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class MyAuthenticationForm(forms.Form):
    username=forms.CharField(
        widget=forms.TextInput(
            attrs={
                "required":True,
                "max_length":30,
                "class":"form-control input-sm",
                "placeholder":"Username",
                "type":"text",
            }
        ),
    )
    password=forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                "required":True,
                "max_length":30,
                "class":"form-control input-sm",
                "placeholder":"Password",
                "type":"password",
            }
        )
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Incorrect username and password. "
                           "Note that both fields may be case-sensitive.")
        if not user.is_active:
            raise forms.ValidationError("This account is inactive.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class RegistrationForm(forms.Form):

    username = forms.RegexField(
        regex=r'^\w+$', widget=forms.TextInput(
            attrs={
                "required":True,
                "max_length":30,
                "class":"form-control input-sm",
                "placeholder":"Username",
                "type":"text",
            }
        ),
        label=_("Username"),
        error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") }
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "required":True,
                "max_length":30,
                "class":"form-control input-sm",
                "placeholder":"Email",
                "type":"email",
            }
        ),
        label=_("Email address")
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "required":True,
                "max_length":30,
                "class":"form-control input-sm",
                "placeholder":"Password",
                "type":"password",
                "render_value":False,
            }
        ),
        label=_("Password")
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "required":True,
                "max_length":30,
                "class":"form-control input-sm",
                "placeholder":"Password again",
                "type":"password",
                "render_value":False,
            }
        ),
        label=_("Password (again)")
    )

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

class PublicIdForm(forms.Form):
    public_id = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "id":"publicIdEditor",
                "style":"display: none; font-size: 36px; line-height: 36px; height: 45px; width: 300px;",
                "class":"form-control",
            }
        )
    )