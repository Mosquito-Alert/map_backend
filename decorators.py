from .constants import (allowed_origins)
from django.http import HttpResponseForbidden
import functools

def deny_empty_origin(view_func):
    """
    this decorators ensures that the view func accepts only 
    XML HTTP Request i.e request done via fetch or ajax
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        origin = request.headers.get('origin')
        if origin in allowed_origins:
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden()
    return wrapper