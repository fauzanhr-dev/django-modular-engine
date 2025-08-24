from functools import wraps
from django.http import HttpResponseForbidden
from .models import Module


def require_installed(app_key: str):
    def deco(viewfunc):
        @wraps(viewfunc)
        def _wrapped(request, *args, **kwargs):
            if not Module.objects.filter(key=app_key, is_installed=True).exists():
                return HttpResponseForbidden('Module is not installed.')
            return viewfunc(request, *args, **kwargs)
        return _wrapped
    return deco