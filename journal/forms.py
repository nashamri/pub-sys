from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Affiliation, Article, Review, AuthorResponse

class ArticleSubmissionForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = [
            'author', 
            'submission_date', 
            'acceptance_date', 
            'publication_date',
            'decision',  # Also exclude decision as it should be set by editors/system
            'reviewers'  # Exclude the reviewers field
        ]  # These fields are set in the view or by the system
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pdf_file'].required = True  # Make PDF upload required
        self.fields['pdf_file'].widget.attrs.update({
            'accept': 'application/pdf',  # Only accept PDF files
            'class': 'file-input'  # Add Bulma class for styling
        })
        # Add help text to make it clear this is a file upload
        self.fields['pdf_file'].help_text = "Upload your article as a PDF file (required)"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['status', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 6, 'class': 'textarea', 'placeholder': 'Optional comments about the article'}),
            'status': forms.Select(attrs={'class': 'select'})
        }



class AuthorResponseForm(forms.ModelForm):
    review_id = forms.IntegerField(widget=forms.HiddenInput())
    
    class Meta:
        model = AuthorResponse
        fields = ['response_text', 'revised_pdf', 'review_id']
        widgets = {
            'response_text': forms.Textarea(attrs={
                'rows': 6, 
                'class': 'textarea', 
                'placeholder': 'Your response to the reviewer comments'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['revised_pdf'].required = False
        self.fields['revised_pdf'].widget.attrs.update({
            'accept': 'application/pdf',
            'class': 'file-input'
        })
        self.fields['revised_pdf'].help_text = "Upload a revised version of your article (optional)"

class ReviewerAssignmentForm(forms.Form):
    """Form for assigning reviewers to articles."""
    reviewers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Reviewers"
    )
    
    def __init__(self, *args, article=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only users who:
        # 1. Are not the author of the article
        # 2. Are not staff or superusers (admins)
        if article:
            self.fields['reviewers'].queryset = User.objects.filter(
                is_staff=False, 
                is_superuser=False
            ).exclude(id=article.author.id)
            # Pre-select currently assigned reviewers
            self.fields['reviewers'].initial = article.reviewers.all()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    affiliation = forms.ModelChoiceField(
        queryset=Affiliation.objects.all(),
        required=False,
        empty_label="Select existing affiliation (or enter new below)"
    )
    new_affiliation_name = forms.CharField(
        max_length=255, required=False, label="New Affiliation Name"
    )
    new_affiliation_country = forms.CharField(
        max_length=100, required=False, label="New Affiliation Country"
    )
    new_affiliation_address = forms.CharField(
        widget=forms.Textarea, required=False, label="New Affiliation Address"
    )
    new_affiliation_phone = forms.CharField(
        max_length=20, required=False, label="New Affiliation Phone"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'affiliation', 'new_affiliation_name', 'new_affiliation_country', 'new_affiliation_address', 'new_affiliation_phone']

    def clean(self):
        cleaned_data = super().clean()
        affiliation = cleaned_data.get('affiliation')
        new_name = cleaned_data.get('new_affiliation_name')
        new_country = cleaned_data.get('new_affiliation_country')

        if not affiliation and not (new_name and new_country):
            raise forms.ValidationError(
                "Please select an existing affiliation or enter at least a name and country for a new one."
            )
        return cleaned_data

