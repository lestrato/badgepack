from django import forms
from django.utils.translation import ugettext_lazy as _

from badge.models import BadgeClass

class BadgeCreationForm(forms.Form):
    image = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "required":True,
                # This is a kind of hacky way to overlay an image over the input
                # Sorry, styling gods
                "style":"height: 150px; width: 150px; \
                    opacity: 0; position: absolute;",
                "class":"badgeImageUpload",
                "type":"file",
            }
        )
    )

    name=forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "required":True,
                "maxlength":20,
                "class":"form-control input-sm",
                "placeholder":"Badge name",
                "type":"text",
                "id":"addBadgeName",
                "name":"addBadgeName",
            }
        ),
    )

    description = forms.CharField(
        max_length=140,
        widget=forms.Textarea(
            attrs={
                "required":True,
                "style":"resize: vertical; height:100px;",
                "class":"form-control",
                "maxlength":140,
                "placeholder":"Badge description",
                "type":"text",
            }
        ),
    )

    def clean(self):
        return self.cleaned_data


class UserBadgeAssignForm(forms.Form):
    CHOICES= (
    ('nothing', 'Nothing'),
    ('gift', 'Gift'),
    )
    badge_assign = forms.CharField(
        widget=forms.Select(
            choices=CHOICES,
            attrs={
                "class":"form-control",
            }
        )
    )

    def clean_badge_assign(self):
        badge_assign = self.cleaned_data.get("badge_assign")
        return badge_assign

class OneBadgeAssignForm(forms.Form):
    badge_assign = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
            }
        )
    )

class BadgeSetAvailabilityForm(forms.Form):
    CHOICES= (
    (False, 'unavailable'),
    (True, 'available'),
    )
    availability = forms.CharField(
        widget=forms.Select(
            choices=CHOICES,
            attrs={
                "class":"form-control",
            }
        )
    )

    def clean_badge_assign(self):
        badge_assign = self.cleaned_data.get("availability")
        return badge_assign
