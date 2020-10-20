from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from store.models import Tecnico, OrdenMantenimiento, Cliente, DetalleOrden, Empresa, RevisionTecnica
from store.forms import OrdenMantenimientoForm, ClienteForm, DetalleOrdenForm, TecnicoForm, RevisionTecnicaForm
from people.models import Usuario
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied


class CustomUserOnlyMixin(object):
    """
    Permite personalizar los permisos de acceso a las vistas
    """
    permissions_required = None

    def has_permissions(self):
        if self.request.user.is_active is False:
            return False
        if self.request.user.is_superuser:
            return True
        groups = self.request.user.groups.all()
        for permissions_required in self.permissions_required:
            for group in groups:
                for permission in group.permissions.all():
                    if permission.codename == permissions_required:
                        return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise PermissionDenied
        return super(CustomUserOnlyMixin, self).dispatch(
            request, *args, **kwargs)


class OrdenListView(LoginRequiredMixin, CustomUserOnlyMixin, ListView):
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
    permissions_required = ('view_ordenmantenimiento',)

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


class OrdenCreateView(SuccessMessageMixin, LoginRequiredMixin, CustomUserOnlyMixin, CreateView):
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
    permissions_required = ('add_ordenmantenimiento',)

    def form_valid(self, form):
        empresa = Empresa.objects.first()
        if empresa is None:
            raise ValidationError("Debe agregar datos de empresa")
        form.instance.empresa_id = empresa.id
        return super().form_valid(form)


class OrdenUpdateView(SuccessMessageMixin, LoginRequiredMixin, CustomUserOnlyMixin, UpdateView):
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
    permissions_required = ('change_ordenmantenimiento',)

    def form_valid(self, form):
        empresa = Empresa.objects.first()
        if empresa is None:
            raise ValidationError("Debe agregar datos de empresa")
        form.instance.empresa_id = empresa.id
        return super().form_valid(form)


class OrdenDeleteView(DeleteView, LoginRequiredMixin, CustomUserOnlyMixin):
    """
    Permite eliminar órdenes de mantenimiento
    **Context**

    ``OrdenMantenimiento``
        An instance of :model:`store.OrdenMantenimiento`.

    **Template:**

    :template:`ordenMantenimiento/delete.html`
    """
    model = OrdenMantenimiento
    template_name = 'delete.html'
    success_url = reverse_lazy('orders')
    permissions_required = ('delete_ordenmantenimiento',)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('orders')
            return HttpResponseRedirect(url)
        else:
            return super(OrdenDeleteView, self).post(request, *args, **kwargs)


class ClienteListView(LoginRequiredMixin, CustomUserOnlyMixin, ListView):
    """
    Permite listar clientes
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
    permissions_required = ('view_cliente',)

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


class ClienteCreateView(SuccessMessageMixin, LoginRequiredMixin, CustomUserOnlyMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    paginate_position = 'Both'
    search_fields = ['nombre__icontains']
    template_name = 'cliente/edit.html'
    success_message = 'Cliente creado con exito'
    permissions_required = ('add_cliente',)

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


class ClienteUpdateView(SuccessMessageMixin, LoginRequiredMixin, CustomUserOnlyMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/edit.html'
    success_url = reverse_lazy('orders')
    success_message = 'Cliente actualizado con exito'
    permissions_required = ('change_cliente',)

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


class ClienteDeleteView(DeleteView, LoginRequiredMixin, CustomUserOnlyMixin):
    model = Cliente
    template_name = 'delete.html'
    success_url = reverse_lazy('clients')
    permissions_required = ('delete_cliente',)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('clients')
            return HttpResponseRedirect(url)
        else:
            return super(ClienteDeleteView, self).post(request, *args, **kwargs)


class TecnicoListView(LoginRequiredMixin, CustomUserOnlyMixin, ListView):
    """
    Permite listar técnicos
    **Context**

    ``Tecnico``
        An instance of :model:`store.Tecnico`.

    **Template:**

    :template:`tecnico/index.html`
    """
    model = Tecnico
    template_name = 'tecnico/index.html'
    context_object_name = 'tecnicos'
    paginate_by = 20
    queryset = Tecnico.objects.all()
    permissions_required = ('view_tecnico',)

    def get_queryset(self):
        new_context = self.queryset
        if self.request.GET.get('filter'):
            new_context = new_context.filter(
                Q(nombre__icontains=self.request.GET.get('filter')) | Q(
                    apellido__icontains=self.request.GET.get('filter'))
            )
        return new_context

    def get_context_data(self, **kwargs):
        context = super(TecnicoListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get(
            'filter') if self.request.GET.get('filter') else ''
        return context


class TecnicoCreateView(SuccessMessageMixin, LoginRequiredMixin, CustomUserOnlyMixin, CreateView):
    model = Tecnico
    form_class = TecnicoForm
    paginate_position = 'Both'
    search_fields = ['nombre__icontains']
    template_name = 'tecnico/edit.html'
    success_message = 'Técnico creado con exito'
    permissions_required = ('add_tecnico',)

    def get_success_url(self, *args, **kwargs):
        return reverse('technicians')

    def form_valid(self, form):
        cleaned_data = form.clean()
        group = Group.objects.get(name='TECNICO')
        usuario = Usuario(nombre_de_usuario=cleaned_data.get("correo_electronico"),
                          is_staff=1, correo_electronico=cleaned_data.get("correo_electronico"))
        tecnico = form.save()
        usuario.persona_id = tecnico.id
        usuario.password = make_password(form.instance.numero_identificacion)
        usuario.save()
        group.user_set.add(usuario)
        return super().form_valid(form)


class TecnicoUpdateView(SuccessMessageMixin, LoginRequiredMixin, CustomUserOnlyMixin, UpdateView):
    model = Tecnico
    form_class = TecnicoForm
    template_name = 'tecnico/edit.html'
    success_url = reverse_lazy('technicians')
    success_message = 'Técnico actualizado con exito'
    permissions_required = ('change_tecnico',)

    def get_success_url(self, *args, **kwargs):
        return reverse('technician-update', kwargs={'pk': self.kwargs['pk']})

    def get_initial(self):
        initial = super(TecnicoUpdateView, self).get_initial()
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


class TecnicoDeleteView(DeleteView, LoginRequiredMixin, CustomUserOnlyMixin):
    model = Tecnico
    template_name = 'delete.html'
    success_url = reverse_lazy('technicians')
    permissions_required = ('delete_tecnico',)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('technicians')
            return HttpResponseRedirect(url)
        else:
            return super(TecnicoDeleteView, self).post(request, *args, **kwargs)


class DetalleOrdenListView(LoginRequiredMixin, CustomUserOnlyMixin, ListView):
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
    permissions_required = ('view_detalleOrden',)

    def get_queryset(self):
        new_context = self.queryset.filter(
            orden_mantenimiento__id=self.kwargs['order_id'])
        if self.request.GET.get('filter'):
            new_context = new_context.filter(
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

    def get_success_url(self):
        return reverse('order-detail-update', kwargs={'order_id': self.kwargs['order_id'], 'pk': self.object.pk, })

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
        context['order_detail_id'] = self.kwargs['pk']
        return context


class DetalleOrdenDeleteView(DeleteView, LoginRequiredMixin):
    model = DetalleOrden
    template_name = 'delete.html'

    def get_context_data(self, **kwargs):
        context = super(DetalleOrdenDeleteView,
                        self).get_context_data(**kwargs)
        context['order_id'] = self.kwargs['order_id']
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('order-details', kwargs={'order_id': self.kwargs['order_id']})

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy(
                'order-details',  kwargs={'order_id': self.kwargs['order_id']})
            return HttpResponseRedirect(url)
        else:
            return super(DetalleOrdenDeleteView, self).post(request, *args, **kwargs)


class RevisionTecnicaListView(LoginRequiredMixin, CustomUserOnlyMixin, ListView):
    """
    Permite listar revisiones técnicas
    **Context**

    ``RevisionTecnica``
        An instance of :model:`store.RevisionTecnica`.

    **Template:**

    :template:`revisionTecnica/index.html`
    """
    model = RevisionTecnica
    template_name = 'revisionTecnica/index.html'
    context_object_name = 'revisiones'
    paginate_by = 20
    queryset = RevisionTecnica.objects.all()
    permissions_required = ('view_revisionTecnica',)

    def get_queryset(self):
        new_context = self.queryset.filter(
            detalle_orden__id=self.kwargs['order_detail_id'])
        if self.request.GET.get('filter'):
            new_context = new_context.filter(
                Q(descripcion__icontains=self.request.GET.get('filter')))
        return new_context

    def get_context_data(self, **kwargs):
        context = super(RevisionTecnicaListView,
                        self).get_context_data(**kwargs)
        context['order_id'] = self.kwargs['order_id']
        context['order_detail_id'] = self.kwargs['order_detail_id']
        context['filter'] = self.request.GET.get(
            'filter') if self.request.GET.get('filter') else ''
        return context


class RevisionTecnicaCreateView(SuccessMessageMixin, LoginRequiredMixin, CustomUserOnlyMixin, CreateView):
    model = RevisionTecnica
    form_class = RevisionTecnicaForm
    paginate_position = 'Both'
    search_fields = ['tecnico__apellido__icontains']
    template_name = 'revisionTecnica/edit.html'
    success_message = 'Revisión Técnica creada con exito'
    permissions_required = ('add_revisiontecnica',)

    def get_success_url(self, *args, **kwargs):
        return reverse('revisions', kwargs={'order_id': self.kwargs['order_id'], 'order_detail_id': self.kwargs['order_detail_id']})

    def get_context_data(self, **kwargs):
        context = super(RevisionTecnicaCreateView,
                        self).get_context_data(**kwargs)
        context['order_detail_id'] = self.kwargs['order_detail_id']
        context['order_id'] = self.kwargs['order_id']
        return context

    def form_valid(self, form):
        form.instance.detalle_orden_id = self.kwargs['order_detail_id']
        return super().form_valid(form)


class RevisionTecnicaUpdateView(SuccessMessageMixin, CustomUserOnlyMixin, LoginRequiredMixin, UpdateView):
    model = RevisionTecnica
    form_class = RevisionTecnicaForm
    template_name = 'revisionTecnica/edit.html'
    success_url = reverse_lazy('revisions')
    success_message = 'Revisión Técnica actualizada con exito'
    permissions_required = ('change_revisiontecnica',)

    def get_success_url(self, *args, **kwargs):
        return reverse('revisions', kwargs={'order_id': self.kwargs['order_id'], 'order_detail_id': self.kwargs['order_detail_id']})

    def get_context_data(self, **kwargs):
        context = super(RevisionTecnicaUpdateView,
                        self).get_context_data(**kwargs)
        context['order_detail_id'] = self.kwargs['order_detail_id']
        context['order_id'] = self.kwargs['order_id']
        return context

    def form_valid(self, form):
        form.instance.detalle_orden_id = self.kwargs['order_detail_id']
        return super().form_valid(form)


class RevisionTecnicaDeleteView(DeleteView, LoginRequiredMixin, CustomUserOnlyMixin):
    model = RevisionTecnica
    template_name = 'delete.html'

    def get_context_data(self, **kwargs):
        context = super(RevisionTecnicaDeleteView,
                        self).get_context_data(**kwargs)
        context['order_detail_id'] = self.kwargs['order_detail_id']
        context['order_id'] = self.kwargs['order_id']
        return context

    def get_success_url(self, **kwargs):
        return reverse('revisions', kwargs={'order_id': self.kwargs['order_id'], 'order_detail_id': self.kwargs['order_detail_id']})

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse('revisions', kwargs={
                          'order_id': self.kwargs['order_id'], 'order_detail_id': self.kwargs['order_detail_id']})
            return HttpResponseRedirect(url)
        else:
            return super(RevisionTecnicaDeleteView, self).post(request, *args, **kwargs)


class RevisionTecnicaPorTecnicoListView(LoginRequiredMixin, CustomUserOnlyMixin, ListView):
    """
    Permite listar revisiones técnicas
    **Context**

    ``RevisionTecnica``
        An instance of :model:`store.RevisionTecnica`.

    **Template:**

    :template:`tecnico/revisionTecnica/index.html`
    """
    model = RevisionTecnica
    template_name = 'tecnico/revisionTecnica/index.html'
    context_object_name = 'revisiones'
    paginate_by = 20
    queryset = RevisionTecnica.objects.all()
    permissions_required = ('view_revisiontecnica',)

    def get_queryset(self):
        new_context = self.queryset.all()
        if self.request.user.persona:
            new_context = new_context.filter(
                tecnico__id=self.request.user.persona_id)
            if self.request.GET.get('filter'):
                new_context = new_context.filter(
                    Q(descripcion__icontains=self.request.GET.get('filter')))
        return new_context

    def get_context_data(self, **kwargs):
        context = super(RevisionTecnicaPorTecnicoListView,
                        self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get(
            'filter') if self.request.GET.get('filter') else ''
        return context
