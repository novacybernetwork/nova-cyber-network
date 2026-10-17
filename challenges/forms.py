from django import forms


class FlagSubmitForm(forms.Form):
    flag = forms.CharField(
        max_length=255,
        label="Flag",
        widget=forms.TextInput(attrs={"placeholder": "NOVA{...}", "autocomplete": "off"}),
    )
