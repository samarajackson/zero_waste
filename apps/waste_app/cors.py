"""
Nothing to see here... ~_~

Temporary workaround for getting cors working locally
Replace with a dev proxy for development and remove all this

"""


class CorsMiddleware(object):
    def process_response(self, response):
        response["Access-Control-Allow-Origin"] = "http://localhost:8080"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS,POST,PUT,DELETE"
        response[
            "Access-Control-Allow-Headers"
        ] = "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers, X-CSRFToken"
        return response

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return self.process_response(response)
