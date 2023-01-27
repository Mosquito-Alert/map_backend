from .constants import (allowed_referers)
from django.http import HttpResponseForbidden
import functools

def referrer_cookie_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.COOKIES.get('referrer') is None:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)

    return wrapper
    

def deny_empty_origin(view_func):
    """
    this decorators ensures that the view func accepts only 
    certain referers
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        origin = request.headers.get('referer')
        try:
            for e in allowed_referers:
                if e in origin:
                    return view_func(request, *args, **kwargs)
        except Exception as e:
            return HttpResponseForbidden()

        return HttpResponseForbidden()
    return wrapper