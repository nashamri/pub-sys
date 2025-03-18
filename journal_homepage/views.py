from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required

def group_required(group_name):
    def check_group(user):
        return user.groups.filter(name=group_name).exists()
    return user_passes_test(check_group)


def homepage(request):
    context = {
        'is_author': request.user.groups.filter(name='author').exists(),
        'is_reviewer': request.user.groups.filter(name='reviewer').exists(),
    }
    return render(request, 'journal_homepage/homepage.html', context)

@login_required
@group_required('author')
def author_home(request):
    return render(request, 'journal_homepage/author_home.html')

@login_required
@group_required('reviewer')
def reviewer_home(request):
    return render(request, 'journal_homepage/reviewer_home.html')


