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
    # input class="hidden" type="file" style="margin-left:20%;" placeholder="Picture" id="badgeImageUpload"

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
