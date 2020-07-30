from django.contrib import auth
from django.contrib.auth import load_backend
from django.contrib.auth.backends import RemoteUserBackend
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser 
from django.http import HttpResponse
from apps.waste_app.models import User

def get_user(request):
    print('called get user')
    print(request.session.items())
    request.user = User.objects.get(id=request.session['userid'])
    print('got user')
    return request.user

def get_user(request):
    userid = request.session.get('userid')
    if userid:
        user = User.objects.get(id=userid)
        if user:
            return user
    return AnonymousUser()


class MyAuthenticationMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )
        request.user = SimpleLazyObject(lambda: get_user(request))
        if hasattr(request, "data"):
            request.data["userid"] = request.user.id
        

# class MyAuthenticationMiddleware(object):
#     def process_request(self, request):
#         assert hasattr(request, 'session'), (
#             "The Django authentication middleware requires session middleware "
#             "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
#             "'django.contrib.sessions.middleware.SessionMiddleware' before "
#             "'django.contrib.auth.middleware.AuthenticationMiddleware'."
#         )
#         print('called process_request')
#         print(request.session.items())
#         if "userid" in request.session:

#         if hasattr(request, 'data') and :
#             request.user = get_user(request)
#             request.data= SimpleLazyObject(lambda: request.user)
    
#     def __init__(self, get_response):
#         self.get_response = get_response
    
#     def __call__(self, request):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.
#         response = self.get_response(request)
#         # Code to be executed for each request/response after
#         # the view is called.
#         request = self.process_request(request)
#         return response