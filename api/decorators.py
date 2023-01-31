from .constants import (allowed_referers)
from django.http import HttpResponseForbidden
import functools

def referrer_cookie_required(view_func):
    """
    this decorator ensures that the view func accepts only 
    session requests
    """        
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.COOKIES.get('sessionid') is None:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)

    return wrapper
