from django import forms

from apps.core.models import Account


class AccountForm(forms.ModelForm):
    email = forms.CharField(required=True, widget=forms.EmailInput)

    class Meta:
        model = Account
        fields = ["marketing_optin"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].initial = self.instance.user.email

    def save(self, *args, **kwargs):
        account = super().save(*args, **kwargs)
        account.user.email = self.cleaned_data["email"]
        account.user.save()
        return account
