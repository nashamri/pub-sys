from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('author_home/', views.author_home, name='author_home'),
    path('reviewer_home/', views.reviewer_home, name='reviewer_home'),

]