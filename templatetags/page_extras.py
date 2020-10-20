from django import template

register = template.Library()


@register.simple_tag()
def has_permission(user, permission_required):
    """
    Permite validar un permiso dentro de un template
    """
    if user.is_active is False:
        return False
    if user.is_superuser is True:
        return True
    groups = user.groups.all()
    for group in groups:
        for permission in group.permissions.all():
            if permission.codename == permission_required:
                return True
    return False
