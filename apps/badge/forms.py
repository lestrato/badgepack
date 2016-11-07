from django import forms

class BadgeCreationForm(forms.Form):
    image = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "required":True,
                "class":"hidden",
                "id":"badgeImageUpload",
                "type":"file",
            }
        ),
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
            }
        ),
    )

    description = forms.CharField(
        max_length=140,
        widget=forms.Textarea(
            attrs={
                "style":"resize: vertical; height:100px;",
                "class":"form-control",
                "maxlength":140,
                "placeholder":"Badge description",
                "type":"text",
            }
        ),
    )


    def clean_description(self):
        description = self.cleaned_data.get("description")
        return description

    def clean_name(self):
        name = self.cleaned_data.get('username')
        return name
        # check to see if name exists
        # try:
        #     user = BadgeClass.objects.get(name__iexact=name)
        # except BadgeClass.DoesNotExist:
        #     return name
        # raise forms.ValidationError(_("The badge name already exists. Please try another one."))

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
