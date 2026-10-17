from django import forms

from .models import Team


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Team name", "maxlength": 80}),
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "Optional team description"}),
        }


class TeamJoinForm(forms.Form):
    invite_code = forms.CharField(max_length=16, label="Invite code")


class TeamManageForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}
