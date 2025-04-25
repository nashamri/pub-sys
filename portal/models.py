from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


# class MyModel(models.Model):
#     upload = models.FileField()
class UploadedFile(models.Model):
    upload = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)


 

articletypes = [
    ('', 'Select a type'),  # Empty default option
    ('a', 'a.'),
    ('b', 'b.'),
    ('c', 'c.'),
 
]

STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('revision_required', 'Revision Required'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

class Submission(models.Model):

    submission_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    article_type = models.CharField(max_length=50)
    abstract = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
 

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # editor = models.ForeignKey('Users', on_delete=models.CASCADE,
    #                            related_name='edited_submissions', blank=True, null=True)
    current_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='submitted')
    # current_review = models.ForeignKey(
    #     'Review', on_delete=models.SET_NULL, blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Review(models.Model):
    DECISION_CHOICES = [
        ('pending', 'Pending'),
        ('accept', 'Accept'),
        ('reject', 'Reject'),
        ('revision_required', 'Revision Required'),
    ]

    review_id = models.AutoField(primary_key=True)
    submission = models.ForeignKey(
        'Submission', on_delete=models.CASCADE, related_name='reviews')
    review_round = models.IntegerField(default=1)
    previous_review = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    decision = models.CharField(
        max_length=20, choices=DECISION_CHOICES, default='pending')
    decision_comments = models.TextField(blank=True, null=True)
    # editor = models.ForeignKey(
    #     'Users', on_delete=models.CASCADE, related_name='conducted_reviews')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.review_id} for {self.submission.title} (Round {self.review_round})"

 

    @property
    def active_reviewers(self):
        # Get all reviewers assigned to this review
        return self.reviews.select_related('reviewer').all()

    @property
    def get_submission_id(self):
        return self.submission.submission_id

    def get_reviewers_by_decision_comments(self, has_comments=True):
        # Filter by whether they have provided comments or not
        return self.reviews.select_related('reviewer').filter(
            decision_comments__isnull=not has_comments
        )

    def get_pending_reviewers(self):
        # Get reviewers who haven't submitted comments yet
        return self.reviews.select_related('reviewer').filter(
            decision_comments__isnull=True
        )

    def get_completed_reviewers(self):
        # Get reviewers who have submitted comments
        return self.reviews.select_related('reviewer').filter(
            decision_comments__isnull=False
        )

def default_due_date():
    return datetime.now() + timedelta(days=30)


class Reviewer(models.Model):
    DECISION_CHOICES = [
        ('pending', 'Pending'),
        ('accept', 'Accept'),
        ('reject', 'Reject'),

    ]

    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    review_id = models.ForeignKey(
        'Review', on_delete=models.CASCADE, related_name='reviews')
    start_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(
         blank=True, null=True)
    decision_comments = models.TextField(blank=True, null=True)

    @property
    def get_review_id(self):
        return self.review_id.review_id

# class ReviewInvitation(models.Model):
#     DECISION_CHOICES = [
#         ('pending', 'Pending'),
#         ('accept', 'Accept'),
#         ('reject', 'Reject'),
         
#     ]

#     id = models.AutoField(primary_key=True)
#     review_id = models.ForeignKey(
#         'Review', on_delete=models.CASCADE, related_name='reviews')
#     start_date = models.DateTimeField(auto_now_add=True)
#     due_date = models.DateTimeField(
#         default=default_due_date, blank=True, null=True)
#     decision = models.CharField(
#         max_length=20, choices=DECISION_CHOICES, default='pending')
 
class SubmissionFile(models.Model):
    review = models.ForeignKey(
        Review, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.file.name
