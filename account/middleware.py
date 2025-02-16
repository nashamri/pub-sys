from django.shortcuts import redirect

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of URLs that logged-in users shouldn't access
        restricted_urls = ['/login/', '/signup/']
        
        if request.user.is_authenticated and request.path in restricted_urls:
            return redirect('/')
            
        response = self.get_response(request)
        return response