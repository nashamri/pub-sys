# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required, user_passes_test
# from django.views.decorators.http import require_POST
# from django.http import JsonResponse
# from .models import UploadedFile

# # Define permission check as a reusable function


# def is_editor(user):
#     """Check if a user is in the Editor group."""
#     return user.groups.filter(name='Editor').exists()


# def is_author(user):
#     """Check if a user is in the Editor group."""
#     return user.groups.filter(name='Author').exists()

# # Define a custom decorator for editor-only views


# def editor_required(view_func):
#     """Decorator that checks if user is an editor."""
#     decorated_view = user_passes_test(
#         is_editor,
#         login_url=None,
#         redirect_field_name=None
#     )(view_func)
#     return decorated_view


# def author_required(view_func):
#     """Decorator that checks if user is an editor."""
#     decorated_view = user_passes_test(
#         is_author,
#         login_url=None,
#         redirect_field_name=None
#     )(view_func)
#     return decorated_view


# @login_required
# @require_POST
# def upload_file(request):
#     """Handle file uploads from authenticated users."""
#     if 'file' not in request.FILES:
#         return JsonResponse({
#             'status': 'error',
#             'message': 'No file received'
#         }, status=400)

#     try:
#         file = request.FILES['file']
#         uploaded_file = UploadedFile(upload=file, uploaded_by=request.user)
#         uploaded_file.save()

#         return JsonResponse({
#             'status': 'success',
#             'message': 'File uploaded successfully'
#         })
#     except Exception as e:
#         return JsonResponse({
#             'status': 'error',
#             'message': str(e)
#         }, status=500)


# @login_required
# @require_POST
# def toggle_mode(request):
#     """Toggle between upload and viewer modes."""
#     if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
#         return JsonResponse({
#             'status': 'error',
#             'message': 'Invalid request'
#         }, status=400)

#     current_mode = request.session.get('portal_mode', 'author')
#     new_mode = 'editor' if current_mode == 'author' else 'author'

#     # If changing to viewer mode, check if user has editor permission
#     if new_mode == 'author' and not is_author(request.user):
#         return JsonResponse({
#             'status': 'error',
#             'message': 'You need Editor permissions to view files.'
#         }, status=403)

#     request.session['portal_mode'] = new_mode
#     return JsonResponse({
#         'status': 'success',
#         'mode': new_mode
#     })


# @login_required
# def portal(request):
#     """Main portal view handling both upload and viewer modes."""
#     # Set default mode if not already set
#     mode = request.session.get('portal_mode', 'upload')

#     # Check user permissions once
#     user_is_editor = is_editor(request.user)
#     user_is_author = is_author(request.user)

#     # Prepare context with common data
#     context = {
#         'active_tab': mode,
#         'is_editor': user_is_editor,
#     }

#     # Add viewer-specific data if applicable
#     if mode == 'viewer':
#         if user_is_editor:
#             context['files'] = UploadedFile.objects.all().order_by(
#                 '-uploaded_at')
#         else:
#             context['permission_error'] = "You need Editor permissions to view files."
#             # Redirect to upload mode since user doesn't have viewer permissions
#             request.session['portal_mode'] = 'author'
#             context['active_tab'] = 'author'

#     return render(request, 'portal/portal.html', context)
