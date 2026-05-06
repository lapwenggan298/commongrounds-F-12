from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import ImproperlyConfigured, PermissionDenied

class RoleRequiredMixin(AccessMixin):
    required_role = None

    def dispatch(self, request, *args, **kwargs):
        if self.required_role is None:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the required_role attribute."
            )

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not hasattr(request.user, 'profile') or request.user.profile.role != self.required_role:
            self.raise_exception = True 
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)