# project/myapp/views.py
from django.http import HttpResponse
from django.shortcuts import redirect

def custom_404(request, exception):
    #return HttpResponse('Hey there, page not found', status=404)
    return redirect('/')

 