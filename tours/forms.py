from django import forms
from django.utils import timezone

from .models import Booking, ContactMessage


class BookingForm(forms.ModelForm):
    # Honeypot field – real users never see or fill this.
    # Bots often fill every field, so we reject submissions that contain a value.
    website = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "tabindex": "-1",
                "aria-hidden": "true",
                "style": "position:absolute;left:-9999px;height:0;width:0;opacity:0;",
            }
        ),
    )

    class Meta:
        model = Booking
        fields = [
            "full_name",
            "email",
            "phone",
            "number_of_people",
            "preferred_date",
            "message",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-field",
                    "placeholder": "Your full name",
                    "autocomplete": "name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-field",
                    "placeholder": "you@example.com",
                    "autocomplete": "email",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-field",
                    "placeholder": "+256 700 000 000",
                    "autocomplete": "tel",
                    "inputmode": "tel",
                }
            ),
            "number_of_people": forms.NumberInput(
                attrs={
                    "class": "form-field",
                    "min": 1,
                }
            ),
            "preferred_date": forms.DateInput(
                attrs={
                    "class": "form-field",
                    "type": "date",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-field",
                    "rows": 4,
                    "placeholder": "Interests, questions or special requirements",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["preferred_date"].widget.attrs["min"] = (
            timezone.localdate().isoformat()
        )

    def clean_preferred_date(self):
        preferred_date = self.cleaned_data.get("preferred_date")
        if preferred_date and preferred_date < timezone.localdate():
            raise forms.ValidationError(
                "Please choose today or a future travel date."
            )
        return preferred_date

    def clean(self):
        cleaned_data = super().clean()
        # Reject if honeypot was filled (bots)
        if cleaned_data.get("website"):
            raise forms.ValidationError(
                "Unable to process your request. Please try again."
            )
        return cleaned_data


class ContactForm(forms.ModelForm):
    # Honeypot field – real users never see or fill this.
    website = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "tabindex": "-1",
                "aria-hidden": "true",
                "style": "position:absolute;left:-9999px;height:0;width:0;opacity:0;",
            }
        ),
    )

    class Meta:
        model = ContactMessage
        fields = ["full_name", "email", "subject", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-field"}),
            "email": forms.EmailInput(attrs={"class": "form-field"}),
            "subject": forms.TextInput(attrs={"class": "form-field"}),
            "message": forms.Textarea(attrs={"class": "form-field", "rows": 6}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("website"):
            raise forms.ValidationError(
                "Unable to process your request. Please try again."
            )
        return cleaned_data
