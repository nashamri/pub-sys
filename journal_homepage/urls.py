from django.urls import path,include
from . import views
from portal.views import portal

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('portal/', portal, name='portal'),

]