from django.urls import path
from . import views

app_name = 'portal'  # This enables URL namespacing

urlpatterns = [
    path('portal/', views.portal, name='portal_default'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('toggle_mode/', views.toggle_mode, name='toggle_mode'),
]
