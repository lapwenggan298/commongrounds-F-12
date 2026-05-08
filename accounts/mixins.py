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

        has_profile = hasattr(request.user, 'profile')
        if not has_profile or not request.user.profile.roles.filter(name=self.required_role).exists():
            self.raise_exception = True 
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)