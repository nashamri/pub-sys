from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('signup_test/', views.signup_test, name='signup_test'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile_view'),
]