from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from django.contrib.auth import logout
from django.contrib import messages


def logout_view(request):
    messages.get_messages(request).used = True  # Clear messages
    logout(request)
    return redirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login user
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'account/login.html')


def signup_view(request):
    if request.method == "POST":
        # Get data from POST
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Create new user
            # Django hashes password automatically
            user = User.objects.create_user(
                username=username,
                password=password
            )
            # Log user in after signup
            login(request, user)
            request.session['user_id'] = user.id
            return redirect('/')  # Redirect to home page after signup

        except IntegrityError:
            # Username already exists
            return render(request, 'account/signup.html', {
                'message': 'Username already taken!',
                'error': True
            })
        except Exception as e:
            # Other errors
            return render(request, 'account/signup.html', {
                'message': f'Error creating account: {str(e)}',
                'error': True
            })

    # GET request - show signup form
    return render(request, 'account/signup.html', {
        'message': 'Please sign up!'
    })
