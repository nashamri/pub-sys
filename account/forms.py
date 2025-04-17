from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Affiliation

class UserRegistrationForm(UserCreationForm):
    # User personal information
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    # Affiliation fields
    affiliation_name = forms.CharField(max_length=255, required=True, 
        help_text="Name of your institution/organization")
    affiliation_address = forms.CharField(widget=forms.Textarea, required=True,
        help_text="Full address of your institution/organization")
    affiliation_country = forms.CharField(max_length=100, required=True)
    affiliation_phone = forms.CharField(max_length=50, required=True,
        help_text="Contact phone number with country code")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',
                 'affiliation_name', 'affiliation_address', 'affiliation_country', 'affiliation_phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            # Create and save the affiliation
            affiliation = Affiliation.objects.create(
                name=self.cleaned_data['affiliation_name'],
                address=self.cleaned_data['affiliation_address'],
                country=self.cleaned_data['affiliation_country'],
                phone=self.cleaned_data['affiliation_phone']
            )

        return user