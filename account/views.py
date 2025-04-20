import ast
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from django.db import IntegrityError
from django.contrib.auth import logout
from django.contrib import messages

from account.forms import AuthorForm
import base64


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


def signup_test(request):
    if request.method == 'POST':
      
        messages.success(
            request, 'Your author account has been created successfully!')
        # Redirect to homepage or another appropriate page
        return redirect('home')

    # If it's a GET request, just render the form template
    return render(request, 'account/mutilform.html')



def register(request):
    if request.method == 'POST':
        current_step = int(request.POST.get('step', 1))

        if current_step == 1:
            user_form = UserCreationForm(request.POST)
            if user_form.is_valid():
                user_clean_data = str(user_form.cleaned_data)
                user_dict = ast.literal_eval(user_clean_data)
                data = f"{user_dict['username']}={user_dict['password1']}"
                b = base64.b64encode(
                    data.encode('utf-8')).decode('utf-8')
                return render(request, 'account/register.html', {
                    'crd': b,  # Pass the entire POST data
                    'author_form': AuthorForm(),
                    'step': 2
                })
            else:
                return render(request, 'account/register.html', {
                    'user_form': user_form,
                    'step': 1
                })

        elif current_step == 2:
            user_clean_data = request.POST.get('crd')
            decoded_bytes = base64.b64decode(user_clean_data)
            decoded_string = decoded_bytes.decode('utf-8')
            # Split the decoded string to get username and password
            username, password = decoded_string.split('=')

            # Create the user
            
            #user_form = UserCreationForm(request.POST)
            #user_form.is_valid() 
            #user = user_form.save()  # Create the User here
            # Now handle the Author form
            author_form = AuthorForm(request.POST)
            if author_form.is_valid():
                user = User.objects.create_user(
                username=username,
                password=password
            )
                author = author_form.save(commit=False)
                author.user = user
                author.save()

                messages.success(request, 'Registration successful!')
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'account/register.html', {
                    'crd': user_clean_data,
                    'author_form': author_form,
                    'step': 2
                })

    return render(request, 'account/register.html', {
        'user_form': UserCreationForm(),
        'step': 1
    })
