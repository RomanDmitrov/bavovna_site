from django import forms
from .models import BookingRequest, PartnershipRequest


class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = ['name', 'email', 'phone', 'telegram', 'category', 'guests', 'budget', 'message']


class PartnershipRequestForm(forms.ModelForm):
    class Meta:
        model = PartnershipRequest
        fields = ['name', 'email', 'phone', 'telegram', 'partnership_type', 'message']