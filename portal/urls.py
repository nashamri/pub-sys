from django.urls import path
from . import views

app_name = 'portal'  # This enables URL namespacing

urlpatterns = [
    path('portal/', views.portal, name='portal_default'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('toggle_mode/', views.toggle_mode, name='toggle_mode'),
    path('submit_manuscript/', views.submit_manuscript, name='submit_manuscript'),
    path('editor_portal/', views.Editor_portal, name='editor_portal'),
    path('editor_portal/<int:submission_id>/',
         views.editor_assignment_details, name='editor_assignment_details'),
    path('editor_portal/new_assignments/',
         views.new_assignments, name='new_assignments'),

    path('editor_portal/<int:submission_id>/assign_reviewer/',
         views.assign_reviewer, name='assign_reviewer'),
         
    path('editor_portal/<int:submission_id>/remove_reviewer/<int:reviewer_id>',
         views.remove_reviewer, name='remove_reviewer'),


 
    path('reviewer/new_assignments/',
         
         views.rev_new_assignments, name='rev_new_assignments'),
         
    path('reviewer/new_assignments/<int:submission_id>/',
         views.reviewer_assignment_details, name='reviewer_assignment_details'),

]
