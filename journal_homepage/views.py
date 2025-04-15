from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import ResearchPaper
from django.contrib import messages

def is_reviewer(user):
    is_in_group = user.groups.filter(name='Reviewer').exists()
    print(f"User {user.username} is reviewer: {is_in_group}")  # للتصحيح
    return is_in_group

@login_required
@user_passes_test(is_reviewer)
def reviewer_dashboard(request):
    # للتصحيح
    print(f"Current user: {request.user.username}")
    
    # الأوراق البحثية المرسلة حديثاً
    new_papers = ResearchPaper.objects.filter(
        reviewer=request.user,
        status='pending'
    )
    print(f"Pending papers: {new_papers.count()}")  # للتصحيح
    
    # الأوراق تحت المراجعة
    in_review_papers = ResearchPaper.objects.filter(
        reviewer=request.user,
        status='in_review'
    )
    print(f"In review papers: {in_review_papers.count()}")  # للتصحيح
    
    # الأوراق المنتهية
    completed_papers = ResearchPaper.objects.filter(
        reviewer=request.user,
        status='completed'
    )
    print(f"Completed papers: {completed_papers.count()}")  # للتصحيح
    
    context = {
        'new_papers': new_papers,
        'in_review_papers': in_review_papers,
        'completed_papers': completed_papers
    }
    
    return render(request, 'journal_homepage/reviewer_dashboard.html', context)

def homepage(request):
    return render(request, 'journal_homepage/homepage.html', {'message': 'Welcome to our Journal'})