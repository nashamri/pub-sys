from django.shortcuts import render

  
def homepage(request):
    return render(request, 'journal_homepage/homepage.html', {'message': 'Welcome to our Journal'})