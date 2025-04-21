from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash # Import auth functions, add update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test # Import login_required decorator and user_passes_test
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm # Import Django's built-in login and password change forms
from django.contrib.auth.models import User
from django.utils import timezone  # Import timezone for setting dates
from django.db.models import Max
from .forms import UserRegisterForm, ArticleSubmissionForm, ReviewForm, AuthorResponseForm, ReviewerAssignmentForm # Import the forms
from .models import Review, Article, AuthorResponse, Profile, Affiliation, Article

@login_required
def submissions_page(request):
    # Prevent admin users from accessing this page
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "This page is not available for admin users.")
        return redirect('assignment_page')
    
    # Get all articles submitted by the current user
    user_articles = Article.objects.filter(author=request.user).order_by('-submission_date')
    return render(request, 'journal/submissions.html', {'articles': user_articles})

@login_required
def article_detail(request, article_id):
    """View for authors to see article details, reviews, and submit responses."""
    article = get_object_or_404(Article, id=article_id)
    
    # Check if the user is the author of this article
    if request.user != article.author:
        messages.error(request, "You are not authorized to view this article.")
        return redirect('submissions_page')
    
    # Get all reviews for this article
    reviews = Review.objects.filter(article=article).order_by('reviewer', '-revision')
    
    # Group reviews by reviewer (showing only the latest revision from each reviewer)
    latest_reviews = {}
    for review in reviews:
        if review.reviewer_id not in latest_reviews:
            latest_reviews[review.reviewer_id] = review
    
    # Convert to list for template
    latest_reviews = list(latest_reviews.values())
    
    if request.method == 'POST':
        # Get the review ID from the form
        review_id = request.POST.get('review_id')
        review = get_object_or_404(Review, id=review_id, article=article)
        
        # Create a new response
        response = AuthorResponse(
            article=article,
            review=review,
            response_text=request.POST.get('response_text', '')
        )
        
        # Handle file upload if provided
        if 'revised_pdf' in request.FILES:
            response.revised_pdf = request.FILES['revised_pdf']
            # If a revised PDF was uploaded, update the article's PDF
            article.pdf_file = response.revised_pdf
            article.decision = 'under_review'  # Reset to under review
            article.save()
        
        response.save()
        
        messages.success(request, "Your response has been submitted successfully.")
        return redirect('article_detail', article_id=article.id)
    
    # Get previous responses by the author
    responses = AuthorResponse.objects.filter(article=article).order_by('-created_at')
    
    return render(request, 'journal/article_detail.html', {
        'article': article,
        'reviews': latest_reviews,
        'responses': responses
    })

@login_required
def reviewer_page(request):
    # Prevent admin users from accessing this page
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "This page is not available for admin users.")
        return redirect('admin_page')
    
    # Get all articles assigned to the current user for review
    # Use distinct() to prevent duplicate articles
    assigned_articles = Article.objects.filter(reviewers=request.user).order_by('-submission_date').distinct()
    return render(request, 'journal/reviewer.html', {'assigned_articles': assigned_articles})

@login_required
def review_article(request, article_id):
    """Handle submission of a review for an article."""
    article = get_object_or_404(Article, id=article_id)
    
    # Check if the user is assigned as a reviewer for this article
    if request.user not in article.reviewers.all():
        messages.error(request, "You are not authorized to review this article.")
        return redirect('reviewer_page')
    
    # Get the latest revision number for this reviewer and article
    latest_revision = Review.objects.filter(
        article=article, 
        reviewer=request.user
    ).aggregate(Max('revision'))['revision__max'] or 0
    
    # For a new review, increment the revision number
    # This will be 1 for the first actual review submission
    new_revision = latest_revision + 1
    
    # Flag to indicate if this is the first review (no previous reviews exist)
    is_first_review = latest_revision == 0
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.article = article
            review.reviewer = request.user
            review.revision = new_revision
            review.save()
            
            # Update article decision based on review status
            # Only update if all reviewers have accepted or at least one has rejected
            all_reviewers = article.reviewers.all()
            latest_reviews = {}
            
            # Get the latest review from each reviewer
            for reviewer in all_reviewers:
                latest_review = Review.objects.filter(
                    article=article,
                    reviewer=reviewer
                ).order_by('-revision').first()
                
                if latest_review:
                    latest_reviews[reviewer.id] = latest_review
            
            # Check if all reviewers have accepted
            if all(review.status == 'accepted' for review in latest_reviews.values()):
                article.decision = 'accepted'
                article.save()
            # Check if any reviewer has rejected
            elif any(review.status == 'rejected' for review in latest_reviews.values()):
                article.decision = 'rejected'
                article.save()
            # If any reviewer has requested corrections, mark as revision requested
            elif any(review.status in ['minor_corrections', 'major_corrections'] for review in latest_reviews.values()):
                article.decision = 'revision_requested'
                article.save()
                
            messages.success(request, "Your review has been submitted successfully.")
            return redirect('reviewer_page')
    else:
        form = ReviewForm()
    
    # Get previous reviews by this reviewer for this article
    previous_reviews = Review.objects.filter(
        article=article, 
        reviewer=request.user
    ).order_by('-revision')
    
    # Get all author responses for this article
    responses = AuthorResponse.objects.filter(article=article).order_by('-created_at')
    
    # We're removing the all_reviews context variable to ensure reviewers only see their own reviews
    return render(request, 'journal/review_article.html', {
        'form': form,
        'article': article,
        'previous_reviews': previous_reviews,
        'responses': responses,
        'revision': new_revision,
        'is_first_review': is_first_review
    })

@login_required
def submit_article(request):
    """Handles article submission by authors."""
    # Prevent admin users from accessing this page
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "This page is not available for admin users.")
        return redirect('admin_page')
    
    if request.method == 'POST':
        form = ArticleSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.submission_date = timezone.now().date()  # Set submission date to today
            article.save()
            messages.success(request, 'Article submitted successfully!')
            return redirect('submissions_page')
    else:
        form = ArticleSubmissionForm()
    return render(request, 'journal/submit_article.html', {'form': form})


# Create your views here.
def home_page(request):
    """Renders the journal home page."""
    return render(request, 'journal/home.html')

def about_page(request):
    """Renders the about page."""
    return render(request, 'journal/about.html')

def guidelines_page(request):
    """Renders the Guidelines page."""
    return render(request, 'journal/guidelines.html')


def register_page(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Determine affiliation
            affiliation = form.cleaned_data.get('affiliation')
            new_name = form.cleaned_data.get('new_affiliation_name')
            new_country = form.cleaned_data.get('new_affiliation_country')
            new_address = form.cleaned_data.get('new_affiliation_address')
            new_phone = form.cleaned_data.get('new_affiliation_phone')
            if not affiliation and new_name and new_country:
                affiliation, created = Affiliation.objects.get_or_create(
                    name=new_name.strip(),
                    country=new_country.strip(),
                    defaults={'address': new_address, 'phone': new_phone}
                )
            # Create Profile
            Profile.objects.create(user=user, affiliation=affiliation)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('home_page')
        # If form is invalid, fall through to render below
    else:
        form = UserRegisterForm()
    return render(request, 'journal/register.html', {'form': form})

def login_page(request):
    """Handles user login."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                # Redirect to a success page, e.g., home page
                return redirect('home_page')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    else:
        # GET request, display an empty login form
        form = AuthenticationForm()
    return render(request, 'journal/login.html', {'form': form})

def logout_page(request):
    """Handles user logout."""
    if request.method == 'POST': # Ensure logout is triggered by POST to prevent accidental logout via GET
        logout(request)
        messages.success(request, "You have been successfully logged out.")
        return redirect('home_page')
    else:
        # If accessed via GET, just redirect to home (or show an error/confirmation page)
        return redirect('home_page')

@login_required # Decorator to ensure user is logged in
def account_page(request):
    """Handles account management, starting with password change."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Important: Update the session auth hash to prevent the user
            # from being logged out after changing their password.
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('account_page') # Redirect back to account page after success
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        # GET request, display an empty form bound to the user
        form = PasswordChangeForm(request.user)
    return render(request, 'journal/account.html', {'form': form})

# Helper function to check if user is admin
def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def assignment_page(request):
    """Assignment page for managing articles and reviewers."""
    # Get all articles ordered by submission date (newest first)
    articles = Article.objects.all().order_by('-submission_date')
    return render(request, 'journal/assignment_page.html', {'articles': articles})

@login_required
@user_passes_test(is_admin)
def assign_reviewers(request, article_id):
    """Handle reviewer assignment for a specific article."""
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        form = ReviewerAssignmentForm(request.POST, article=article)
        if form.is_valid():
            # Clear existing reviewers and add the selected ones
            article.reviewers.clear()
            selected_reviewers = form.cleaned_data['reviewers']
            for reviewer in selected_reviewers:
                article.reviewers.add(reviewer)
            
            messages.success(request, f"Reviewers successfully assigned to '{article.title}'")
            return redirect('admin_page')
    else:
        form = ReviewerAssignmentForm(article=article)
    
    return render(request, 'journal/assign_reviewers.html', {
        'form': form,
        'article': article
    })

@login_required
@user_passes_test(is_admin)
def article_revisions(request, article_id):
    """View for admins to see all revisions and responses for an article."""
    article = get_object_or_404(Article, id=article_id)
    
    # Get all reviews for this article, ordered by reviewer and revision
    reviews = Review.objects.filter(article=article).order_by('reviewer', 'revision')
    
    # Group reviews by reviewer
    reviewers_data = {}
    for review in reviews:
        if review.reviewer_id not in reviewers_data:
            reviewers_data[review.reviewer_id] = {
                'username': review.reviewer.username,
                'reviews': []
            }
        reviewers_data[review.reviewer_id]['reviews'].append(review)
    
    # Get all author responses
    responses = AuthorResponse.objects.filter(article=article).order_by('-created_at')
    
    return render(request, 'journal/article_revisions.html', {
        'article': article,
        'reviewers_data': reviewers_data,
        'responses': responses
    })
