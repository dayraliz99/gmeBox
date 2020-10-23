from django.contrib import admin
from people.models import Direccion

from store.models import (Categoria, Empresa, Producto,
                          Proveedor, OrdenMantenimiento, DetalleOrden, RevisionTecnica, Compra, DetalleCompra)
import nested_admin


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


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'empresa')
    search_fields = ('nombre', 'empresa')
    list_filter = ('nombre', 'empresa')
    fieldsets = (
        (('Información de Categoría'), {'fields': (
            'nombre', 'descripcion', 'empresa')}),
    )


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad', 'descripcion', 'categoria')
    search_fields = ('nombre', 'categoria')
    list_filter = ('nombre', 'categoria')


class RevisionTecnicaAdminInline(nested_admin.NestedTabularInline):
    model = RevisionTecnica
    extra = 1


class DetalleOrdenInline(nested_admin.NestedTabularInline):
    model = DetalleOrden
    inlines = (RevisionTecnicaAdminInline,)
    extra = 1


class OrdenMantenimientoAdmin(nested_admin.NestedModelAdmin):
    list_display = ('fecha_registro', 'estado', 'descripcion', 'cliente')
    search_fields = ('descripcion', 'estado')
    list_filter = ('descripcion', 'estado', 'cliente')
    inlines = (DetalleOrdenInline,)


admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(OrdenMantenimiento, OrdenMantenimientoAdmin)
