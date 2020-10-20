from django.core.exceptions import PermissionDenied


class CustomUserOnlyMixin(object):
    """
    Permite personalizar los permisos de acceso para los views
    """
    permissions_required = None

    def has_permissions(self):
        if self.request.user.is_active is False:
            return False
        if self.request.user.is_superuser is True:
            return True
        groups = self.request.user.groups.all()
        for permission_required in self.permissions_required:
            for group in groups:
                for permission in group.permissions.all():
                    if permission.codename == permission_required:
                        return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise PermissionDenied
        return super(CustomUserOnlyMixin, self).dispatch(
            request, *args, **kwargs)
