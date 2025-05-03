from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('about/', views.about_page, name='about_page'),
    path('guidelines/', views.guidelines_page, name='guidelines_page'),
    path('register/', views.register_page, name='register_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'), # Add logout URL
    path('account/', views.account_page, name='account_page'), # Add account management URL
    path('submissions/', views.submissions_page, name='submissions_page'),
    path('reviewer/', views.reviewer_page, name='reviewer_page'),
    path('submit/', views.submit_article, name='submit_article'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('review/<int:article_id>/', views.review_article, name='review_article'),
    path('assignment/', views.assignment_page, name='assignment_page'),
    path('assignment/assign/<int:article_id>/', views.assign_reviewers, name='assign_reviewers'),
    path('assignment/revisions/<int:article_id>/', views.article_revisions, name='article_revisions'),
    path('accepted-articles/', views.accepted_articles, name='accepted_articles'),
    ]





