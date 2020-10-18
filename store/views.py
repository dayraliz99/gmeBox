from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from store.models import Tecnico, OrdenMantenimiento, Cliente, DetalleOrden, Empresa
from store.forms import OrdenMantenimientoForm, ClienteForm, DetalleOrdenForm
from people.models import Usuario
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView
from django.urls import reverse
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import Group


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
                    cliente__apellido__icontains=self.request.GET.get('filter')) | Q(
                        cliente__nombre__icontains=self.request.GET.get('filter')) | Q(
                        cliente__numero_identificacion__icontains=self.request.GET.get('filter')))

        return new_context

    def get_context_data(self, **kwargs):
        context = super(OrdenListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get(
            'filter') if self.request.GET.get('filter') else ''
        return context


class OrdenCreateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Permite crear órdenes de mantenimiento
    **Context**

    ``OrdenMantenimiento``
        An instance of :model:`store.OrdenMantenimiento`.

    **Template:**

    :template:`ordenMantenimiento/edit.html`
    """
    model = OrdenMantenimiento
    form_class = OrdenMantenimientoForm
    template_name = 'ordenMantenimiento/edit.html'
    success_message = 'Órden creada con exito'
    permission_required = ('add_ordenmantenimiento',)

    def form_valid(self, form):
        empresa = Empresa.objects.first()
        if empresa is None:
            raise ValidationError("Debe agregar datos de empresa")
        form.instance.empresa_id = empresa.id
        return super().form_valid(form)


class OrdenUpdateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Permite editar órdenes de mantenimiento
    **Context**

    ``OrdenMantenimiento``
        An instance of :model:`store.OrdenMantenimiento`.

    **Template:**

    :template:`ordenMantenimiento/edit.html`
    """
    model = OrdenMantenimiento
    form_class = OrdenMantenimientoForm
    template_name = 'ordenMantenimiento/edit.html'
    success_message = 'Órden actualizada con exito'
    permission_required = ('change_ordenmantenimiento',)

    def form_valid(self, form):
        empresa = Empresa.objects.first()
        if empresa is None:
            raise ValidationError("Debe agregar datos de empresa")
        form.instance.empresa_id = empresa.id
        return super().form_valid(form)


class OrdenDeleteView(DeleteView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Permite eliminar órdenes de mantenimiento
    **Context**

    ``OrdenMantenimiento``
        An instance of :model:`store.OrdenMantenimiento`.

    **Template:**

    :template:`ordenMantenimiento/delete.html`
    """
    model = OrdenMantenimiento
    template_name = 'ordenMantenimiento/delete.html'
    success_url = reverse_lazy('orders')
    permission_required = ('delete_ordenmantenimiento',)

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


class ClienteCreateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    paginate_position = 'Both'
    search_fields = ['nombre__icontains']
    template_name = 'cliente/edit.html'
    success_message = 'Cliente creado con exito'
    permission_required = ('add_cliente',)

    def get_success_url(self, *args, **kwargs):
        return reverse('clients')

    def form_valid(self, form):
        cleaned_data = form.clean()
        group = Group.objects.get(name='CLIENTE')
        usuario = Usuario(nombre_de_usuario=cleaned_data.get("correo_electronico"),
                          is_staff=1, correo_electronico=cleaned_data.get("correo_electronico"))
        client = form.save()
        usuario.persona_id = client.id
        usuario.password = make_password(form.instance.numero_identificacion)
        usuario.save()
        group.user_set.add(usuario)
        return super().form_valid(form)


class ClienteUpdateView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/edit.html'
    success_url = reverse_lazy('orders')
    success_message = 'Cliente actualizado con exito'
    permission_required = ('change_cliente',)

    def get_success_url(self, *args, **kwargs):
        return reverse('client-update', kwargs={'pk': self.kwargs['pk']})

    def get_initial(self):
        initial = super(ClienteUpdateView, self).get_initial()
        initial['correo_electronico'] = self.object.usuario.correo_electronico
        return initial

    def form_valid(self, form):
        cleaned_data = form.clean()
        usuario = Usuario.objects.get(persona_id=form.instance.id)
        usuario.correo_electronico = cleaned_data.get("correo_electronico")
        usuario.nombre_de_usuario = cleaned_data.get("correo_electronico")
        usuario.password = make_password(form.instance.numero_identificacion)
        usuario.save()
        return super().form_valid(form)


class ClienteDeleteView(DeleteView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Cliente
    template_name = 'cliente/delete.html'
    success_url = reverse_lazy('clients')
    permission_required = ('delete_cliente',)

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
            new_context = new_context.filter(orden_mantenimiento__id=self.kwargs['order_id']).filter(
                Q(nombre_equipo__icontains=self.request.GET.get('filter')))

        return new_context

    def get_context_data(self, **kwargs):
        context = super(DetalleOrdenListView, self).get_context_data(**kwargs)
        context['order_id'] = self.kwargs['order_id']
        context['filter'] = self.request.GET.get(
            'filter') if self.request.GET.get('filter') else ''
        return context


class DetalleOrdenCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = DetalleOrden
    form_class = DetalleOrdenForm
    template_name = 'detalleOrden/edit.html'
    success_message = 'Detalle creado con exito'
    success_url = reverse_lazy('order-details')

    def get_success_url(self):
        return reverse_lazy('order-details', kwargs={'order_id': self.kwargs['order_id']})

    def get_context_data(self, **kwargs):
        context = super(DetalleOrdenCreateView,
                        self).get_context_data(**kwargs)
        context['order_id'] = self.kwargs['order_id']
        return context

    def form_valid(self, form):
        form.instance.orden_mantenimiento_id = self.kwargs['order_id']
        return super().form_valid(form)


class DetalleOrdenUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = DetalleOrden
    form_class = DetalleOrdenForm
    template_name = 'detalleOrden/edit.html'
    success_message = 'Órden actualizada con exito'

    def get_success_url(self, **kwargs):
        return reverse_lazy('order-details', kwargs={'order_id': self.kwargs['order_id']})

    def get_context_data(self, **kwargs):
        context = super(DetalleOrdenUpdateView,
                        self).get_context_data(**kwargs)
        context['order_id'] = self.kwargs['order_id']
        return context


class DetalleOrdenDeleteView(DeleteView, LoginRequiredMixin):
    model = DetalleOrden
    template_name = 'detalleOrden/delete.html'

    def get_context_data(self, **kwargs):
        context = super(DetalleOrdenDeleteView,
                        self).get_context_data(**kwargs)
        context['order_id'] = self.kwargs['order_id']
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('order-details', kwargs={'order_id': self.kwargs['order_id']})

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('order-details')
            return HttpResponseRedirect(url)
        else:
            return super(DetalleOrdenDeleteView, self).post(request, *args, **kwargs)
