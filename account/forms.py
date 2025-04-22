# forms.py
from django import forms
 
from django.forms import ModelForm
from .models import AffiliationInfo, PersonalInfo
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
class AffiliationInfoForm(forms.ModelForm):
    class Meta:
        model = AffiliationInfo
        fields = [
            'position',
            'institution',
            'department',
            'street_address',
            'city',
            'state_province',
            'zip_postal_code',
            'country_region',
            'address_is_for',
            'available_as_reviewer'
        ]
        widgets = {
            'street_address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(AffiliationInfoForm, self).__init__(*args, **kwargs)
        # Make required fields more obvious
        self.fields['institution'].widget.attrs.update(
            {'class': 'required-field'})
        self.fields['country_region'].widget.attrs.update(
            {'class': 'required-field'})
        self.fields['address_is_for'].widget.attrs.update(
            {'class': 'required-field'})

        # Optional: add placeholders or help text
        self.fields['position'].widget.attrs.update(
            {'placeholder': 'e.g., Professor, Researcher, Student'})
        self.fields['institution'].widget.attrs.update(
            {'placeholder': 'e.g., University of Example'})


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = [
            'title',
            'first_name',
            'middle_name',
            'last_name',
            'degree',
            'email',
            'primary_phone',
            'primary_phone_type',
            'secondary_phone',
            'secondary_phone_type'
        ]

    def __init__(self, *args, **kwargs):
        super(PersonalInfoForm, self).__init__(*args, **kwargs)
        # Mark required fields
        required_fields = ['first_name', 'last_name',
                           'email', 'primary_phone', 'primary_phone_type']
        for field in required_fields:
            self.fields[field].widget.attrs.update({'class': 'required-field'})

        # Add phone format hint
        self.fields['primary_phone'].widget.attrs.update(
            {'placeholder': 'e.g., +1-123-456-7890'})
        self.fields['secondary_phone'].widget.attrs.update(
            {'placeholder': 'e.g., +1-123-456-7890'})


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model=User 
        fields=['username']
        help_texts = {
            'username': None,
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper=FormHelper()
    #     self.helper.id
# class AuthorForm(ModelForm):
    
#     class Meta:
#         model = Author
#         fields = ["name", "title", "birth_date"]


 