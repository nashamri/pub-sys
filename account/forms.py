# forms.py
from django import forms
from .models import Author
from django.forms import ModelForm


class AuthorForm(ModelForm):
    
    class Meta:
        model = Author
        fields = ["name", "title", "birth_date"]


 