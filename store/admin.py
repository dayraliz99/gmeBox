from django.contrib import admin
from people.models import Direccion

from store.models import (Categoria, Empresa, Producto,
                          Proveedor, OrdenMantenimiento, DetalleOrden, RevisionTecnica, Compra, DetalleCompra)
import nested_admin


class DirecionAdminInline(admin.TabularInline):
    model = Direccion


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'mision',
                    'vision', 'contacto', 'email', 'telefono')

    fieldsets = (
        (('Información de Empresa'), {'fields': ('nombre', 'descripcion', 'mision', 'vision', 'contacto', 'email', 'telefono',
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

    def save_model(self, request, obj, form, change):
        obj.calcular_cantidad()
        obj.save()


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


class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    fields = ('producto', 'cantidad', 'precio_unitario', 'impuesto')


class CompraAdmin(admin.ModelAdmin):
    fields = ('fecha_compra', 'proveedor', 'estado',)
    list_display = ('fecha_compra', 'proveedor', 'estado',
                    'subtotal', 'impuesto', 'total')
    search_fields = ('proveedor', 'estado')
    list_filter = ('fecha_compra', 'estado', 'proveedor')
    inlines = (DetalleCompraInline,)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.calcular_total()
            instance.save()
            producto = Producto.objects.get(id=instance.producto.id)
            producto.cantidad = producto.cantidad+instance.cantidad
            producto.save()
        formset.instance.calcular_impuesto()
        formset.instance.calcular_subtotal()
        formset.instance.calcular_total()
        formset.instance.save()


admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(OrdenMantenimiento, OrdenMantenimientoAdmin)
admin.site.register(Compra, CompraAdmin)
