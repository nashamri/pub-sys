from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
  
def homepage(request):
    return render(request, 'journal_homepage/homepage.html')

@permission_required('sessions.author_perm')
def author_home(request):
    return render(request, 'journal_homepage/author_home.html')

@permission_required('sessions.reviewer_perm')
def reviewer_home(request):
    return render(request, 'journal_homepage/reviewer_home.html')

