from django.contrib import admin
from store.models import Empresa, Tecnico, Proveedor, Categoria, Producto, Precio, Impuesto
from people.models import Direccion


class DirecionAdminInline(admin.TabularInline):
    model = Direccion


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contacto', 'email', 'telefono')

    fieldsets = (
        (('Información de Empresa'), {'fields': ('nombre', 'contacto', 'email', 'telefono',
                                                 'celular', 'direccion')}),
    )


class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contacto', 'email',
                    'telefono', 'celular', 'direccion')

    fieldsets = (
        (('Información de Proveedor'), {'fields': (
            'nombre', 'contacto', 'email', 'telefono', 'celular', 'direccion')}),
    )


class TecnicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'numero_identificacion',
                    'tipo_documento_identificacion')
    fieldsets = (
        (('Datos Personales'), {'fields': (
            'nombre', 'apellido', 'numero_identificacion', 'tipo_documento_identificacion')},
         ),
        (('Datos de Técnico'), {'fields': ('fecha_ingreso',)},
         ),
    )
    inlines = (DirecionAdminInline,)


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'empresa')
    search_fields = ('nombre', 'empresa')
    list_filter = ('nombre', 'empresa')
    fieldsets = (
        (('Información de Categoría'), {'fields': (
            'nombre', 'descripcion', 'empresa')}),
    )


class PrecioAdminInline(admin.TabularInline):
    model = Precio


class ImpuestoAdmin(admin.TabularInline):
    model = Impuesto


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad', 'descripcion', 'categoria')
    search_fields = ('nombre', 'categoria')
    list_filter = ('nombre', 'categoria')
    inlines = (PrecioAdminInline, ImpuestoAdmin)


admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Tecnico, TecnicoAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
