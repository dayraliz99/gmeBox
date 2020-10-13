from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from store.models import Tecnico, OrdenMantenimiento
from store.forms import OrdenMantenimientoForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse


class OrdenListView(LoginRequiredMixin, ListView):
    """
    Permite listar las órdenes de mantenimiento
    **Context**

    ``OrdenMantenimiento``
        An instance of :model:`store.OrdenMantenimiento`.

    **Template:**

    :template:`ordenMantenimiento/index.html`
    """
    model = OrdenMantenimiento
    template_name = 'ordenMantenimiento/index.html'
    context_object_name = 'ordenes'
    paginate_by = 10
    queryset = OrdenMantenimiento.objects.all()


class OrdenCreateView(LoginRequiredMixin, CreateView):
    model = OrdenMantenimiento
    form_class = OrdenMantenimientoForm
    template_name = 'ordenMantenimiento/edit.html'
    success_message = 'Órden creada con exito'

    def get_success_url(self, *args, **kwargs):
        return reverse('orders')


class OrdenUpdateView(UpdateView):
    model = OrdenMantenimiento
    form_class = OrdenMantenimientoForm
    template_name = 'ordenMantenimiento/edit.html'
    success_url = reverse_lazy('orders')
    success_message = 'Órden actualizada con exito'
    def get_success_url(self, *args, **kwargs):
        return reverse('order-update', kwargs={'pk': self.kwargs['pk']})


class OrdenDeleteView(DeleteView):
    model = OrdenMantenimiento
    template_name = 'ordenMantenimiento/delete.html'
    success_url = reverse_lazy('orders')
