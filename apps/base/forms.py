from django import forms

class CommunitySearchForm(forms.Form):
    community = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "required":True,
                "max_length":30,
                "class":"form-control input-sm",
                "placeholder":"Search for a community...",
                "type":"text",
                # "id":"csInput",
            }
        ),
    )

    def clean(self):
        return self.cleaned_data
