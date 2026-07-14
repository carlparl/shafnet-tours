from django import forms
from .models import Booking, ContactMessage

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['full_name', 'email', 'phone', 'number_of_people', 'preferred_date', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500',
                'placeholder': 'your@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500',
                'placeholder': '+256 XXX XXX XXX'
            }),
            'number_of_people': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500',
                'min': 1
            }),
            'preferred_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500',
                'type': 'date'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500',
                'rows': 4,
                'placeholder': 'Any special requests or questions?'
            }),
        }
        labels = {
            'number_of_people': 'Number of People',
            'preferred_date': 'Preferred Travel Date (optional)',
            'message': 'Additional Message (optional)',
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['full_name', 'email', 'subject', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl', 'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl', 'placeholder': 'your@email.com'}),
            'subject': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl', 'placeholder': 'Subject (optional)'}),
            'message': forms.Textarea(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl', 'rows': 5, 'placeholder': 'Your message...'}),
        }