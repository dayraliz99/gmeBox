from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from store.models import Tecnico, OrdenMantenimiento
from store.forms import OrdenMantenimientoForm
from django.http import HttpResponseRedirect


@login_required()
def index(request):
    """
    Permite listar las órdenes de mantenimiento
    **Context**

    ``OrdenMantenimiento``
        An instance of :model:`store.OrdenMantenimiento`.

    **Template:**

    :template:`ordenMantenimiento/index.html`
    """
    ordenes = OrdenMantenimiento.objects.all()
    return render(request, 'ordenMantenimiento/index.html', locals())


@login_required()
def editar_orden(request, orden_id):
    form = OrdenMantenimientoForm()
    if request.method == 'POST':
        form = OrdenMantenimientoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/store/ordenes')
    return render(request, 'ordenMantenimiento/edit.html', locals())
