from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from people.models import Usuario
from people.forms import (CustomAdminPasswordChangeForm, UserChangeForm,
                          UserCreationForm)


class UsuarioAdmin(auth_admin.UserAdmin):
    add_form = UserCreationForm
    change_password_form = CustomAdminPasswordChangeForm
    fieldsets = (
        (None, {'fields': ('correo_electronico', 'password', 'persona')}),

        ('Permissions', {'fields': ('is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', )}),
    )
    limited_fieldsets = (
        (None, {'fields': ('correo_electronico',)}),

        ('Important dates', {'fields': ('last_login', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('persona', 'correo_electronico', 'password1', 'password2')}
         ),
    )
    list_display = ('correo_electronico', 'persona')
    ordering = ('correo_electronico',)

    list_filter = ('correo_electronico',)
    search_fields = (
        'persona__numero_identificacion', 'persona__nombre', 'persona__apellido')


admin.site.register(Usuario, UsuarioAdmin)
