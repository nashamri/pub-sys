from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Affiliation(models.Model):
    """Represents an affiliation like a university or institution."""
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True) # Use TextField for potentially long addresses, allow blank
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True) # Use CharField for phone numbers, allow blank

    def __str__(self):
        return self.name

class Profile(models.Model):
    """Profile model to store additional user information."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    affiliation = models.ForeignKey(Affiliation, on_delete=models.SET_NULL, null=True, blank=True, related_name='profiles')

    def __str__(self):
        return f"Profile for {self.user.username}"

class Article(models.Model):
    """Model to store information about articles."""
    ARTICLE_TYPE_CHOICES = [
        ('original', 'Original Article'),
        ('review', 'Review Article'),
    ]
    DECISION_CHOICES = [
        ('accepted', 'Accepted'),
        ('under_review', 'Under review'),
        ('revision_requested', 'Revision Requested'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    type = models.CharField(max_length=20, choices=ARTICLE_TYPE_CHOICES)
    pdf_file = models.FileField(upload_to='article_pdfs/', null=True, blank=True, help_text="Upload your article as a PDF file")
    submission_date = models.DateField()
    acceptance_date = models.DateField(null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    decision = models.CharField(max_length=20, choices=DECISION_CHOICES, default='under_review')
    reviewers = models.ManyToManyField(User, through='Review', related_name='reviewing_articles')
    
    def get_current_revision_for_reviewer(self, reviewer):
        """Get the current revision number for a specific reviewer."""
        latest_review = self.reviews.filter(reviewer=reviewer).order_by('-revision').first()
        # Return the revision number if a review exists, otherwise return 0 to indicate no reviews yet
        return latest_review.revision if latest_review else 0
    
    def __str__(self):
        return self.title


class Review(models.Model):
    """Model to store review information for articles."""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('minor_corrections', 'Minor Corrections'),
        ('major_corrections', 'Major Corrections'),
    ]
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    comments = models.TextField(blank=True)  # Make comments optional
    revision = models.PositiveIntegerField(default=0)  # Start at 0, increment for each review round
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Ensure each reviewer can only have one review per revision per article
        unique_together = ['article', 'reviewer', 'revision']
        ordering = ['article', 'reviewer', '-revision']
    
    def __str__(self):
        return f"Review of '{self.article.title}' by {self.reviewer.username} (Rev {self.revision})"


class AuthorResponse(models.Model):
    """Model to store author responses to reviews."""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='responses')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='author_responses')
    response_text = models.TextField()
    revised_pdf = models.FileField(upload_to='revised_pdfs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Response to review of '{self.article.title}' (Rev {self.review.revision})"


