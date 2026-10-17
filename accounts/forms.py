from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, School

INPUT_ATTRS = {"class": "input"}


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(INPUT_ATTRS)
        self.fields["password"].widget.attrs.update(INPUT_ATTRS)


class ClaimAccountForm(UserCreationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs=INPUT_ATTRS))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=INPUT_ATTRS), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=INPUT_ATTRS), label="Confirm password")

    class Meta:
        model = User
        fields = ["username"]

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("That username is already taken.")
        return username


class RequestAccessForm(forms.Form):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs=INPUT_ATTRS))
    email = forms.EmailField(widget=forms.EmailInput(attrs=INPUT_ATTRS))
    school = forms.ModelChoiceField(
        queryset=School.objects.all(), required=False, widget=forms.Select(attrs=INPUT_ATTRS)
    )
    school_other = forms.CharField(
        max_length=150, required=False, label="School (if not listed)", widget=forms.TextInput(attrs=INPUT_ATTRS)
    )

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name"]
        widgets = {"display_name": forms.TextInput(attrs={"class": "input"})}
