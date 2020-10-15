from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from store.models import Tecnico, OrdenMantenimiento, Cliente, DetalleOrden
from store.forms import OrdenMantenimientoForm, ClienteForm, DetalleOrdenForm
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse
from django.db.models import Q


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
    paginate_by = 20
    queryset = OrdenMantenimiento.objects.all()

    def get_queryset(self):
        new_context = self.queryset
        if self.request.GET.get('filter'):
            new_context = new_context.filter(
                Q(descripcion__icontains=self.request.GET.get('filter')) | Q(
                    cliente__apellido__icontains=self.request.GET.get('filter'))
            )
        return new_context

    def get_context_data(self, **kwargs):
        context = super(OrdenListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get(
            'filter') if self.request.GET.get('filter') else ''
        return context


class OrdenCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = OrdenMantenimiento
    form_class = OrdenMantenimientoForm
    template_name = 'ordenMantenimiento/edit.html'
    success_message = 'Órden creada con exito'

    def get_success_url(self, *args, **kwargs):
        return reverse('orders')


class OrdenUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
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

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('orders')
            return HttpResponseRedirect(url)
        else:
            return super(OrdenDeleteView, self).post(request, *args, **kwargs)


class ClienteListView(LoginRequiredMixin, ListView):
    """
    Permite listar los cliente
    **Context**

    ``Cliente``
        An instance of :model:`store.Cliente`.

    **Template:**

    :template:`cliente/index.html`
    """
    model = Cliente
    template_name = 'cliente/index.html'
    context_object_name = 'clientes'
    paginate_by = 20
    queryset = Cliente.objects.all()

    def get_queryset(self):
        new_context = self.queryset
        if self.request.GET.get('filter'):
            new_context = new_context.filter(
                Q(nombre__icontains=self.request.GET.get('filter')) | Q(
                    apellido__icontains=self.request.GET.get('filter'))
            )
        return new_context

    def get_context_data(self, **kwargs):
        context = super(ClienteListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get(
            'filter') if self.request.GET.get('filter') else ''
        return context


class ClienteCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    paginate_position = 'Both'
    search_fields = ['nombre__icontains']
    template_name = 'cliente/edit.html'
    success_message = 'Cliente creado con exito'

    def get_success_url(self, *args, **kwargs):
        return reverse('clients')


class ClienteUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/edit.html'
    success_url = reverse_lazy('orders')
    success_message = 'Cliente actualizado con exito'

    def get_success_url(self, *args, **kwargs):
        return reverse('client-update', kwargs={'pk': self.kwargs['pk']})


class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'cliente/delete.html'
    success_url = reverse_lazy('clients')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('clients')
            return HttpResponseRedirect(url)
        else:
            return super(ClienteDeleteView, self).post(request, *args, **kwargs)


class DetalleOrdenListView(LoginRequiredMixin, ListView):
    """
    Permite listar detalles de órdenes de mantenimiento
    **Context**

    ``DetalleOrden``
        An instance of :model:`store.DetalleOrden`.

    **Template:**

    :template:`detalleOrden/index.html`
    """
    model = DetalleOrden
    template_name = 'detalleOrden/index.html'
    context_object_name = 'detalles'
    paginate_by = 10
    queryset = DetalleOrden.objects.all()

    def get_queryset(self):
        new_context = self.queryset
        if self.request.GET.get('filter'):
            new_context = new_context.filter(
                Q(nombre_equipo__icontains=self.request.GET.get('filter')))

        return new_context

    def get_context_data(self, **kwargs):
        context = super(DetalleOrdenListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get(
            'filter') if self.request.GET.get('filter') else ''
        return context


class DetalleOrdenCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = DetalleOrden
    form_class = DetalleOrdenForm
    template_name = 'detalleOrden/edit.html'
    success_message = 'Detalle creado con exito'
    success_url = reverse_lazy('order-details')


class DetalleOrdenUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = DetalleOrden
    form_class = DetalleOrdenForm
    template_name = 'detalleOrden/edit.html'
    success_url = reverse_lazy('order-details')
    success_message = 'Órden actualizada con exito'


class DetalleOrdenDeleteView(DeleteView):
    model = DetalleOrden
    template_name = 'detalleOrden/delete.html'
    success_url = reverse_lazy('order-details')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('order-details')
            return HttpResponseRedirect(url)
        else:
            return super(DetalleOrdenDeleteView, self).post(request, *args, **kwargs)
