from django import forms
from django.utils import timezone

from .models import Booking, ContactMessage


class BookingForm(forms.ModelForm):
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


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["full_name", "email", "subject", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-field"}),
            "email": forms.EmailInput(attrs={"class": "form-field"}),
            "subject": forms.TextInput(attrs={"class": "form-field"}),
            "message": forms.Textarea(attrs={"class": "form-field", "rows": 6}),
        }
