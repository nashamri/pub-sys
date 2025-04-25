from django import forms
from .models import Submission, SubmissionFile,Review
from django.forms import inlineformset_factory


class SubmissionReviewerForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = [
            'title',
            'article_type',
            'abstract',
            'keywords',
            'current_status'
        ]

       

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make most fields disabled (view-only)
        for field_name, field in self.fields.items():
            field.disabled=True


class SubmissionEditorForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = [
            'title',
            'article_type',
            'abstract',
            'keywords',
            'current_status'
        ]
     
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'article_type': forms.TextInput(attrs={'class': 'form-control'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'keywords': forms.TextInput(attrs={'class': 'form-control'}),
            'current_status': forms.Select(attrs={'class': 'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make most fields disabled (view-only)
        for field_name, field in self.fields.items():
            # Skip fields you want to remain editable
            if field_name not in ['current_status',]:
                field.disabled = True


class DocumentForm(forms.ModelForm):
    class Meta:
        model = SubmissionFile
        fields = ('description', 'file',)

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = [
            'title',
            'article_type',
            'abstract',
            'keywords',
         ]
        exclude = ['current_status','author',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'article_type': forms.TextInput(attrs={'class': 'form-control'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'keywords': forms.TextInput(attrs={'class': 'form-control'}),
            'current_status': forms.Select(attrs={'class': 'form-control'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = []  # No fields needed if just creating a basic review



class FilesForm(forms.ModelForm):
    class Meta:
        model = SubmissionFile
        fields = [
            'file',
            'description',
        ]

 