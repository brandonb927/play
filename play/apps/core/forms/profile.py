from django import forms
from django.db import transaction

from apps.core.models import Profile

BOARD_THEMES = (("light", "Light"), ("dark", "Dark"))


class ProfileForm(forms.ModelForm):
    email = forms.CharField(required=True, widget=forms.EmailInput)

    board_setting_frame_rate = forms.IntegerField(
        required=True, initial=12, max_value=30, min_value=1
    )
    board_setting_theme = forms.ChoiceField(
        required=True, choices=BOARD_THEMES, initial=BOARD_THEMES[0]
    )

    class Meta:
        model = Profile
        fields = ["optin_marketing"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].initial = self.instance.user.email

        try:
            self.fields[
                "board_setting_frame_rate"
            ].initial = self.instance.board_settings["frame_rate"]
        except:
            pass

        try:
            self.fields["board_setting_theme"].initial = self.instance.board_settings[
                "theme"
            ]
        except:
            pass

    @transaction.atomic
    def save(self, *args, **kwargs):
        profile = super().save(*args, **kwargs)
        profile.user.email = self.cleaned_data["email"]
        profile.user.save()

        profile.board_settings["frame_rate"] = self.cleaned_data[
            "board_setting_frame_rate"
        ]
        profile.board_settings["theme"] = self.cleaned_data["board_setting_theme"]

        profile.save()

        return profile
