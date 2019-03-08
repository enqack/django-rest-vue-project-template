from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.contrib.auth.mixins import AccessMixin
from django.db.models.functions import Lower

class GroupRequiredMixin(AccessMixin):
    """Verify that the current user is a member of spcified groups"""
    group_required = None

    def get_group_required(self):
        if self.group_required is None:
            raise ImproperlyConfigured(
                '{0} is missing the group_required attribute. Define {0}.group_required, or override '
                '{0}.get_group_required().'.format(self.__class__.__name__)
            )
        if isinstance(self.group_required, str):
            groups = (self.group_required,)
        else:
            groups = self.group_required
        return groups

    def has_group(self):
        groups = self.get_group_required()
        if self.request.user.groups.filter(name__in=groups).exists():
            return True
        raise PermissionDenied

    def dispatch(self, request, *args, **kwargs):
        if not self.has_group():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
