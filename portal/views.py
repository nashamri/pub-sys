from datetime import datetime, timedelta
from .models import Reviewer, Submission, SubmissionFile
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, modelformset_factory
from portal.forms import FilesForm, ReviewForm, SubmissionEditorForm, SubmissionForm, SubmissionReviewerForm 
from .models import UploadedFile,Review
from django.contrib import messages

# Define permission check as a reusable function


def is_editor(user):
    """Check if a user is in the Editor group."""
    return user.groups.filter(name='Editor').exists()


def is_author(user):
    """Check if a user is in the Editor group."""
    return user.groups.filter(name='Author').exists()


def is_reviewer(user):
    """Check if a user is in the Editor group."""
    return user.groups.filter(name='Reviewer').exists()

# Define a custom decorator for editor-only views


def editor_required(view_func):
    """Decorator that checks if user is an editor."""
    decorated_view = user_passes_test(
        is_editor,
        login_url='/',  # Create this page
        redirect_field_name=None
    )(view_func)
    return decorated_view


def author_required(view_func):
    """Decorator that checks if user is an editor."""
    decorated_view = user_passes_test(
        is_author,
        login_url='/',  # Create this page
        redirect_field_name=None
    )(view_func)
    return decorated_view


def reviewer_required(view_func):
    """Decorator that checks if user is an editor."""
    decorated_view = user_passes_test(
        is_reviewer,
        login_url='/',  # Create this page
        redirect_field_name=None
    )(view_func)
    return decorated_view

@login_required
@require_POST
def upload_file(request):
    """Handle file uploads from authenticated users."""
    if 'file' not in request.FILES:
        return JsonResponse({
            'status': 'error',
            'message': 'No file received'
        }, status=400)

    try:
        file = request.FILES['file']
        uploaded_file = UploadedFile(upload=file, uploaded_by=request.user)
        uploaded_file.save()

        return JsonResponse({
            'status': 'success',
            'message': 'File uploaded successfully'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
@require_POST
def toggle_mode(request):
    """Toggle between upload and viewer modes."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request'
        }, status=400)

    current_mode = request.session.get('portal_mode', 'author')
    new_mode = 'editor' if current_mode == 'author' else 'author'

    # If changing to viewer mode, check if user has editor permission
    if new_mode == 'author' and not is_author(request.user):
        return JsonResponse({
            'status': 'error',
            'message': 'You need Editor permissions to view files.'
        }, status=403)

    request.session['portal_mode'] = new_mode
    return JsonResponse({
        'status': 'success',
        'mode': new_mode
    })


@login_required
def portal(request):
    user = request.user

    user_groups = list(user.groups.values_list('name', flat=True))
    print(user_groups)

    context = {'user_groups': user_groups}
    return render(request, 'portal/portal.html', context)


@login_required
@author_required
def submit_manuscript(request):
    #ReviewFilesSet = modelformset_factory(Review, form=FilesForm,extra=0)
    FilesFormSet = inlineformset_factory(
        parent_model=Review,
        model=SubmissionFile,
        form=FilesForm,
        extra=3,  # Number of empty file forms to show
        can_delete=False
    )

    if request.method == 'POST':
        submission_form = SubmissionForm(request.POST)
        review_form = ReviewForm(request.POST)
        files_formset = FilesFormSet(request.POST, request.FILES)

        if all([submission_form.is_valid(), review_form.is_valid(), files_formset.is_valid()]):
            # 1. Save Submission
            submission = submission_form.save(commit=False)
            submission.author = request.user
            submission.save()

            # 2. Create Review for this Submission
            review = review_form.save(commit=False)
            review.submission = submission
            review.save()

            # 3. Save Files connected to this Review
            files = files_formset.save(commit=False)
            for file in files:
                file.review = review
                file.save()

            messages.success(request, 'Submission created successfully!')
            return redirect('/')  # Change to your success URL

    else:
        submission_form = SubmissionForm()
        review_form = ReviewForm()
        files_formset = FilesFormSet()

    context = {
        'submission_form': submission_form,
        'review_form': review_form,
        'files_formset': files_formset,
    }
    return render(request, 'portal/author/submission.html', context)

    # else:
    #     form = SubmissionForm()
    #     formset = FilesFormSet()

    # #formset = ReviewFilesSet(request.POST or None,)
    # return render(request, 'portal/author/submission.html', {
    #         'form':form,
    #         'formset': formset
    #          })

    # #form = SubmissionForm(initial={'author': request.user.id})
    # if request.method == 'POST':

    #     u_form = SubmissionForm(request.POST)
    #     if u_form.is_valid():
    #         # This creates your submission model instance without saving
    #         submission = u_form.save(commit=False)
    #         submission.author = request.user  # Assign the current user to the author field

    #         submission.save()  # Now save the model

       
    #         messages.success(request, 'Update successful!')
    #         return redirect('/profile')

    # context = {'form': SubmissionForm()}
    # return render(request, 'portal/author/submission.html', context)


@login_required
@editor_required
def Editor_portal(request, submission_id=None):
    from .models import Submission
 
    return render(request, 'portal/editor/editor_main.html', {
       
        'submissions': Submission.objects.all(),
        
    })


@login_required
@editor_required
def editor_assignment_details(request, submission_id=None):
    from .models import Submission
    print('get post!!',submission_id)
     
    submission = get_object_or_404(Submission, pk=submission_id)
    latest_review = submission.reviews.order_by('-review_round').first()
    files = latest_review.files.all() if latest_review else []

    if request.method == 'POST':
        form = SubmissionEditorForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, "Submission updated successfully!")
            return redirect('portal:editor_portal')
    else:
        form = SubmissionEditorForm(instance=submission)
    # submission = Submission.objects.get(pk=submission_id)
    return render(request, 'portal/editor/assignment_details.html', {
        'form': form,
        'submission': submission,  # Pass both the form and submission to template
        'attachments':files

    })


@login_required
@editor_required
def new_assignments(request):
    from .models import Submission
 
    # submission = Submission.objects.get(pk=submission_id)
    return render(request, 'portal/editor/new_assignments.html', {
 
        'submissions': Submission.objects.all(),

    })


@login_required
@editor_required
def assign_reviewer(request, submission_id):
    from .models import Submission
    from django.utils.timezone import now  # Use this instead of datetime.now()

    # Fixed typo: "Reviwer" → "Reviewers"
    submission = get_object_or_404(Submission, pk=submission_id)

    reviewers = User.objects.filter(groups__name="Reviewer")


    latest_review = Review.objects.filter(
        submission=submission
    ).order_by('-created_at').first()  # Note the parentheses to call first()
    print(latest_review.created_at)
 
    current_reviewers = latest_review.active_reviewers
    current_reviewers_ids = User.objects.filter(
        reviewer__review_id=latest_review
    )

    available_reviewers = reviewers.exclude(id__in=current_reviewers_ids)

    print(current_reviewers)
    if request.method == 'POST':
        selected_user_id = request.POST.get('selected_user')
        selected_user = get_object_or_404(User, pk=selected_user_id)
        selected_user_name = selected_user.get_full_name() or selected_user.username

        print('aqaqaqaq', submission_id, selected_user_name)
        # Assign the reviewer

        Reviewer.objects.create(
                    reviewer=selected_user,
                    review_id=latest_review,  # Use the review instance directly
                    due_date=now() + timedelta(days=30) ) # timezone-aware
                    # Update submission status if needed
        if submission.current_status == 'submitted':
            submission.current_status = 'under_review'
            submission.save()
            return redirect('editor_assignment_details', submission_id=submission_id)

    # submission = Submission.objects.get(pk=submission_id)
    return render(request, 'portal/editor/assign_reviewer.html', {
        'submission': submission,
        'reviewers': available_reviewers,
        'assigned_reviewers': current_reviewers,

    })


# @login_required
# @editor_required
# def remove_reviewer(request, submission_id, reviewer_id):
#     print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
#     # latest_review = Review.objects.filter(
#     #     submission_id=submission_id
#     # ).order_by('-created_at').first()

#     # if latest_review:
#     #     try:
#     #         # Updated to match your model relationship
#     #         reviewer_to_remove = Reviewer.objects.get(
#     #             review=latest_review,
#     #             reviewer_id=reviewer_id
#     #         )
#     #         reviewer_to_remove.delete()
#     #         messages.success(request, 'Reviewer removed successfully.')
#     #     except Reviewer.DoesNotExist:
#     #         messages.error(request, 'Reviewer not found.')
#     # else:
#     #     messages.error(request, 'Review not found.')
#     if request.method == 'POST':
#         print('sss', submission_id, reviewer_id)
#         return redirect('portal:assign_reviewer', submission_id=submission_id)

#     return redirect('portal:assign_reviewer', submission_id=submission_id)

@login_required
@editor_required
def remove_reviewer(request, submission_id, reviewer_id):
    # Get the latest review
    latest_review = Review.objects.filter(
        submission_id=submission_id
    ).order_by('-created_at').first()

    if latest_review:
        try:
            # Updated to use review_id instead of review
            reviewer_to_remove = Reviewer.objects.get(
                review_id=latest_review,
                reviewer_id=reviewer_id
            )
            reviewer_to_remove.delete()
            messages.success(request, 'Reviewer removed successfully.')
        except Reviewer.DoesNotExist:
            messages.error(request, 'Reviewer not found.')
        except Reviewer.MultipleObjectsReturned:
            # Handle multiple reviewers case - updated field name here too
            Reviewer.objects.filter(
                review_id=latest_review,
                reviewer_id=reviewer_id
            ).delete()
            messages.success(
                request, 'All matching reviewer entries removed successfully.')
    else:
        messages.error(request, 'Review not found.')

    # Redirect back to the review page
    return redirect('portal:assign_reviewer', submission_id=submission_id)

@login_required
@reviewer_required
def rev_new_assignments(request):
    from .models import Submission
    submissions = Submission.objects.filter(
        reviews__reviews__reviewer=request.user
    ).distinct()

    # if assignments:
    #     # Get submissions from the assignments
    #     submission_ids = assignments.values_list(
    #         'submission__submission_id', flat=True)
    #     submissions = Submission.objects.filter(submission_id__in=submission_ids)
    # else:
    #     return HttpResponse('there is no assignments not found')

    # submission = Submission.objects.get(pk=submission_id)
    return render(request, 'portal/reviewer/new_assignments.html', {

        'submissions': submissions,

    })


@login_required
@reviewer_required
def reviewer_assignment_details(request, submission_id=None):
    from .models import Submission
    print('get post!!', submission_id)

    submission = get_object_or_404(Submission, pk=submission_id)
    latest_review = submission.reviews.order_by('-review_round').first()
    files = latest_review.files.all() if latest_review else []

    if request.method == 'POST':
        form = SubmissionEditorForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, "Submission updated successfully!")
            return redirect('portal:editor_portal')
    else:
        form = SubmissionReviewerForm(instance=submission)
    # submission = Submission.objects.get(pk=submission_id)
    return render(request, 'portal/reviewer/assignment_details.html', {
        'form': form,
        'submission': submission,  # Pass both the form and submission to template
        'attachments': files

    })

 # Filter by author
#  submissions = Submission.objects.filter(
#       author=request.user).order_by('submission_date')
#   submission = submissions.first()
#    # Process form
#    if request.method == 'POST':
#         form = SubmissionEditorForm(request.POST, instance=submission)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Update successful!")
#             return redirect('portal:editor_portal', submission_id=submission.submission_id)
#     else:
#         form = SubmissionEditorForm(instance=submission)

#     return render(request, 'portal/editor/editor_main.html', {
#         'form': form,
#         'submission': submission,
#         'user_submissions': submissions,
#     })
# @login_required
# @editor_required
# def Editor_portal(request):
#     from .models import Submission

#     submissions = Submission.objects.filter(
#         author=request.user).order_by('submission_date')

#     submission = submissions.first()
#     if request.method == 'POST':
#         form = SubmissionEditorForm(request.POST, instance=submission)
#         if form.is_valid():
#             form.save()
#             return redirect('submission_editor', submission_id=submission.id)
#     else:
#         form = SubmissionEditorForm(instance=submission)

#     return render(request, 'portal/editor/editor_main.html', {
#         'form': form,
#         'submission': submission,
#         'user_submissions': submissions,
#     })



#     # user = request.user

    # user_groups = list(user.groups.values_list('name', flat=True))
    # print(user_groups)

    # context = {'form': SubmissionEditorForm}
    # return render(request, 'portal/editor/editor_main.html', context)
