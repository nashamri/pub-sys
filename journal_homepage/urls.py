from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('reviewer/', views.reviewer_dashboard, name='reviewer_dashboard'),
]