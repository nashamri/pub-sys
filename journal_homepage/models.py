from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ResearchPaper(models.Model):
    REVIEW_STATUS = (
        ('pending', 'Pending Assignment'),
        ('in_review', 'Under Review'),
        ('completed', 'Review Completed')
    )

    title = models.CharField(max_length=200)
    abstract = models.TextField()
    file = models.FileField(upload_to='papers/')
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=REVIEW_STATUS, default='pending')
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='papers_to_review')
    review_comments = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
