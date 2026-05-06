from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.conf import settings
from functools import wraps

def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(f"{settings.LOGIN_URL}?next={request.path}")
            
            if hasattr(request.user, 'profile') and request.user.profile.role == required_role:
                return view_func(request, *args, **kwargs)
            
            raise PermissionDenied
            
        return _wrapped_view
    return decorator