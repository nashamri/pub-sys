from django.urls import path
from django.contrib import admin
from django.template.response import TemplateResponse
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import json
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from django.shortcuts import render, redirect
from django.core.files.storage import default_storage


class UserManagement:
    @staticmethod
    def get_users():
        User = get_user_model()
        return User.objects.all().order_by('-date_joined')

    @staticmethod
    def update_user_permissions(user_id, data):
        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
            changed = False

            # Check for changes on the INSTANCE
            if 'is_active' in data and user.is_active != data['is_active']:
                user.is_active = data['is_active']
                changed = True

            if 'is_staff' in data and user.is_staff != data['is_staff']:
                user.is_staff = data['is_staff']
                changed = True

            if 'is_superuser' in data and user.is_superuser != data['is_superuser']:
                user.is_superuser = data['is_superuser']
                changed = True

            # Import models inside the function to avoid AppRegistryNotReady error
            from django.contrib.auth.models import Group, Permission

            # Handle groups
            if 'groups' in data:
                # Clear existing groups and add new ones
                user.groups.clear()
                for group_id in data['groups']:
                    try:
                        group = Group.objects.get(id=group_id)
                        user.groups.add(group)
                        changed = True
                    except Group.DoesNotExist:
                        pass

            # Handle user permissions
            if 'permissions' in data:
                # Clear existing permissions and add new ones
                user.user_permissions.clear()
                for perm_id in data['permissions']:
                    try:
                        permission = Permission.objects.get(id=perm_id)
                        user.user_permissions.add(permission)
                        changed = True
                    except Permission.DoesNotExist:
                        pass

            if changed:
                user.save()
                return True, "User updated successfully"
            else:
                return False, "No changes detected"

        except User.DoesNotExist:
            return False, "User not found"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def get_user_groups_and_permissions(user_id):
        User = get_user_model()
        # Import models inside the function to avoid AppRegistryNotReady error
        from django.contrib.auth.models import Group, Permission

        try:
            user = User.objects.get(id=user_id)

            # Get all available groups and permissions
            all_groups = Group.objects.all()
            all_permissions = Permission.objects.all().select_related('content_type')

            # Get user's current groups and permissions
            user_groups = user.groups.all()
            user_permissions = user.user_permissions.all()

            # Format permissions to make them more readable
            formatted_permissions = []
            for perm in all_permissions:
                formatted_permissions.append({
                    'id': perm.id,
                    'name': f"{perm.content_type.app_label}.{perm.codename}",
                    'description': perm.name,
                    'assigned': perm in user_permissions
                })

            # Format groups
            formatted_groups = []
            for group in all_groups:
                formatted_groups.append({
                    'id': group.id,
                    'name': group.name,
                    'assigned': group in user_groups
                })

            return True, {
                'groups': formatted_groups,
                'permissions': formatted_permissions
            }

        except User.DoesNotExist:
            return False, "User not found"
        except Exception as e:
            return False, str(e)


class AdminInterface(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('users/', self.admin_view(self.user_list), name='user_list'),
            path('files/', self.admin_view(self.files_manager),
                 name='files_manager'),
            path('files/<int:file_id>/delete/',
                 self.admin_view(self.file_delete), name='file_delete'),
            path('files/delete-selected/',
                 self.admin_view(self.delete_selected_files), name='delete_selected_files'),

            path('users/<int:user_id>/update/',
                 self.admin_view(self.update_permissions), name='update_permissions'),
            path('users/<int:user_id>/groups-permissions/',
                 self.admin_view(self.get_groups_and_permissions), name='get_groups_and_permissions'),
        ]
        return my_urls + urls

    def user_list(self, request):
        users = UserManagement.get_users()
        print(users.all()[:1].get().id)
        return TemplateResponse(request, 'admin_interface/index.html', {'users': users})

    def update_permissions(self, request, user_id):
        if request.method == 'POST':
            data = json.loads(request.body)
            success, message = UserManagement.update_user_permissions(
                user_id, data)
            print(success, message)
            return JsonResponse({'success': success, 'message': message})
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    def get_groups_and_permissions(self, request, user_id):
        if request.method == 'GET':
            success, result = UserManagement.get_user_groups_and_permissions(
                user_id)
            if success:
                return JsonResponse({'success': True, 'data': result})
            else:
                return JsonResponse({'success': False, 'message': result})
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    def file_delete(self, request, file_id):
        from portal.models import UploadedFile

        print('deleting file id', file_id)
        if request.method == 'POST':
            try:
                # Get the content type from the request
                content_type = request.META.get('CONTENT_TYPE', '')

                # Handle the data based on content type
                if 'application/json' in content_type:
                    data = json.loads(request.body)
                    filename = data.get('filename')
                else:
                    filename = request.POST.get('filename')

                print(f"Filename: {filename}")

                # Get the file object
                file_obj = UploadedFile.objects.get(id=file_id)

                # Store the file path
                # file_path = file_obj.upload.path

                # Delete the file from storage
                if default_storage.exists(filename):
                    print('file found')
                    default_storage.delete(filename)
                    file_obj.delete()

                # Delete the database record
                current_url = request.META.get('HTTP_REFERER')
                print('--', current_url)
                return redirect(request.META['HTTP_REFERER'])

                # return JsonResponse({'success': True, 'message': 'File deleted successfully'})
            except UploadedFile.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'File not found'}, status=404)
            except Exception as e:
                print(f"Error deleting file: {str(e)}")
                return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)

        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

    decorators = [never_cache,]

    @method_decorator(decorators, name='dispatch')
    def files_manager(self, request):
        from portal.models import UploadedFile
        """Main portal view handling both upload and viewer modes."""
        # Set default mode if not already set

        # Prepare context with common data
        context = {}

        # Add viewer-specific data if applicable
        context['files'] = UploadedFile.objects.all().order_by('-uploaded_at')

        return render(request, 'admin_interface/files_manager.html', context)

    def delete_selected_files(self, request):
        from portal.models import UploadedFile
        from django.http import JsonResponse
        import json

        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                file_ids = data.get('file_ids', [])

                if not file_ids:
                    return JsonResponse({'success': False, 'message': 'No files selected'}, status=400)

                deleted_count = 0
                errors = []

                for file_id in file_ids:
                    try:
                        file_obj = UploadedFile.objects.get(id=file_id)
                        filename = file_obj.upload.name

                        if default_storage.exists(filename):
                            default_storage.delete(filename)

                        file_obj.delete()
                        deleted_count += 1
                    except UploadedFile.DoesNotExist:
                        errors.append(f"File ID {file_id} not found")
                    except Exception as e:
                        errors.append(
                            f"Error deleting file ID {file_id}: {str(e)}")

                if errors:
                    message = f"Deleted {deleted_count} files, but encountered {len(errors)} errors"
                    return JsonResponse({
                        'success': deleted_count > 0,
                        'message': message,
                        'errors': errors
                    })

                return JsonResponse({
                    'success': True,
                    'message': f'Successfully deleted {deleted_count} files'
                })

            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)

        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)
