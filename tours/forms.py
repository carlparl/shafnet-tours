from django import forms
from django.utils import timezone

from .models import Booking, ContactMessage


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['full_name', 'email', 'phone', 'number_of_people', 'preferred_date', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-field',
                'placeholder': 'Your full name',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-field',
                'placeholder': 'you@example.com',
                'autocomplete': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-field',
                'placeholder': '+256 700 000 000',
                'autocomplete': 'tel',
                'inputmode': 'tel',
            }),
            'number_of_people': forms.NumberInput(attrs={
                'class': 'form-field',
                'min': 1,
            }),
            'preferred_date': forms.DateInput(attrs={
                'class': 'form-field',
                'type': 'date',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-field',
                'rows': 4,
                'placeholder': 'Interests, special requirements or questions',
            }),
        }
        labels = {
            'number_of_people': 'Number of People',
            'preferred_date': 'Preferred Travel Date (optional)',
            'message': 'Additional Message (optional)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['preferred_date'].widget.attrs['min'] = timezone.localdate().isoformat()

    def clean_preferred_date(self):
        preferred_date = self.cleaned_data.get('preferred_date')
        if preferred_date and preferred_date < timezone.localdate():
            raise forms.ValidationError('Please choose a current or future travel date.')
        return preferred_date


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['full_name', 'email', 'subject', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-field',
                'placeholder': 'Your full name',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-field',
                'placeholder': 'you@example.com',
                'autocomplete': 'email',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-field',
                'placeholder': 'Safari enquiry, local getaway…',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-field',
                'rows': 7,
                'placeholder': 'Tell us about your dates, group and travel ideas',
            }),
        }
