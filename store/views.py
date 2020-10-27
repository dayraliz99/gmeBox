from datetime import datetime
from django_weasyprint.views import CONTENT_TYPE_PNG
from django_weasyprint import WeasyTemplateResponseMixin
from utils.views import CustomUserOnlyMixin, CustomGroupOnlyMixin
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.urls import reverse
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from people.models import Usuario
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from store.models import (Tecnico, OrdenMantenimiento, Cliente, DetalleOrden, Producto,
                          Empresa, RevisionTecnica, Factura, DetalleFactura, PagoFactura)
from store.forms import (OrdenMantenimientoForm, ClienteForm, DetalleOrdenForm, TecnicoForm, RevisionTecnicaForm, PagoFacturaForm,
                         GestionarRevisionTecnicaForm, OrdenMantenimientoConfirmarForm, FacturaForm, DetalleFacturaForm)


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        empresa = Empresa.objects.first()
        context['empresa'] = empresa
        return context


class GalleryView(TemplateView):
    template_name = "gallery.html"


class ServicioView(TemplateView):
    template_name = "servicio.html"


class ContactoView(TemplateView):
    template_name = "contacto.html"

    def get_context_data(self, **kwargs):
        context = super(ContactoView, self).get_context_data(**kwargs)
        empresa = Empresa.objects.first()
        context['empresa'] = empresa
        return context


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


class OrdenPrintView(LoginRequiredMixin, DetailView):
    model = OrdenMantenimiento
    template_name = 'ordenMantenimiento/print.html'

    def get_context_data(self, **kwargs):
        context = super(OrdenPrintView, self).get_context_data(**kwargs)
        context['title'] = "Detalle de Órden"
        context['asunto'] = "Órden de Mantenimiento"
        context['fecha'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return context


class OrdenDownloadView(WeasyTemplateResponseMixin, OrdenPrintView):
    pdf_filename = 'detalle.pdf'


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
        form.instance.estado = "NUEVO"
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
        form.instance.calcular_monto()
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


class OrdenConfirm(UpdateView, LoginRequiredMixin, CustomGroupOnlyMixin):
    """
    Permite confirmar soporte órdenes de mantenimiento
    **Context**

    ``OrdenMantenimiento``
        An instance of :model:`store.OrdenMantenimiento`.

    **Template:**

    :template:`ordenMantenimiento/confirmSupport.html`
    """
    model = OrdenMantenimiento
    form_class = OrdenMantenimientoConfirmarForm
    template_name = 'ordenMantenimiento/confirmSupport.html'
    success_url = reverse_lazy('orders')
    success_message = 'Órden confirmada con exito'
    groups_required = ('CLIENTE',)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('orders')
            return HttpResponseRedirect(url)
        return super(OrdenConfirm, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.persona_id == form.instance.cliente_id:
            form.instance.confirmar()
            form.instance.estado = "CONFIRMADO"
        else:
            raise PermissionDenied
        return super().form_valid(form)


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
                          is_staff=1, is_active=True, correo_electronico=cleaned_data.get("correo_electronico"))
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
                          is_staff=1, is_active=True, correo_electronico=cleaned_data.get("correo_electronico"))
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


class DetalleOrdenCreateView(SuccessMessageMixin, CustomUserOnlyMixin, LoginRequiredMixin, CreateView):
    model = DetalleOrden
    form_class = DetalleOrdenForm
    template_name = 'detalleOrden/edit.html'
    success_message = 'Detalle creado con exito'
    permissions_required = ('add_detalleorden',)

    def get_success_url(self):
        return reverse('order-detail-update', kwargs={'order_id': self.kwargs['order_id'], 'pk': self.object.pk, })

    def get_context_data(self, **kwargs):
        context = super(DetalleOrdenCreateView,
                        self).get_context_data(**kwargs)
        context['order_id'] = self.kwargs['order_id']
        return context

    def form_valid(self, form):
        orden = OrdenMantenimiento.objects.get(id=self.kwargs['order_id'])
        form.instance.orden_mantenimiento_id = orden.id
        form.save()
        orden.calcular_monto()
        orden.save()
        return super().form_valid(form)


class DetalleOrdenUpdateView(SuccessMessageMixin, CustomUserOnlyMixin, LoginRequiredMixin, UpdateView):
    model = DetalleOrden
    form_class = DetalleOrdenForm
    template_name = 'detalleOrden/edit.html'
    success_message = 'Órden actualizada con exito'
    permissions_required = ('change_detalleOrden',)

    def get_success_url(self, **kwargs):
        return reverse_lazy('order-details', kwargs={'order_id': self.kwargs['order_id']})

    def get_context_data(self, **kwargs):
        context = super(DetalleOrdenUpdateView,
                        self).get_context_data(**kwargs)
        context['order_id'] = self.kwargs['order_id']
        context['order_detail_id'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        form.save()
        orden = OrdenMantenimiento.objects.get(id=self.kwargs['order_id'])
        orden.calcular_monto()
        orden.save()
        return super().form_valid(form)


class DetalleOrdenDeleteView(DeleteView, CustomUserOnlyMixin, LoginRequiredMixin):
    model = DetalleOrden
    template_name = 'delete.html'
    permissions_required = ('delete_detalleOrden',)

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
            detalle = DetalleOrden.objects.get(id=self.kwargs['pk'])
            orden = OrdenMantenimiento.objects.get(id=self.kwargs['order_id'])
            orden.calcular_monto()
            orden.monto_servicio = orden.monto_servicio - detalle.precio_servicio
            orden.save()
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
        detalle = DetalleOrden.objects.get(id=self.kwargs['order_detail_id'])
        detalle.estado = 'EN_REVISION'
        detalle.save()
        orden = OrdenMantenimiento.objects.get(
            id=detalle.orden_mantenimiento_id)
        if orden.verificar_estado_detalles('EN_REVISION'):
            orden.estado = 'EN_REVISION'
        else:
            orden.estado = 'NUEVO'
        orden.save()
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


class RevisionTecnicaPorTecnicoUpdateView(SuccessMessageMixin, CustomUserOnlyMixin, LoginRequiredMixin, UpdateView):
    model = RevisionTecnica
    form_class = GestionarRevisionTecnicaForm
    template_name = 'tecnico/revisionTecnica/edit.html'
    success_url = reverse_lazy('revisions-by-technician')
    success_message = 'Revisión Técnica actualizada con exito'
    permissions_required = ('change_revisiontecnica',)

    def get_initial(self):
        initial = super(RevisionTecnicaPorTecnicoUpdateView,
                        self).get_initial()
        initial['estado'] = self.object.detalle_orden.estado
        return initial

    def form_valid(self, form):
        cleaned_data = form.clean()
        detalle = DetalleOrden.objects.get(id=form.instance.detalle_orden_id)
        detalle.estado = cleaned_data.get("estado")
        detalle.save()
        orden = OrdenMantenimiento.objects.get(
            id=detalle.orden_mantenimiento_id)
        if orden.verificar_estado_detalles(cleaned_data.get("estado")):
            orden.estado = cleaned_data.get("estado")
        else:
            orden.estado = "EN_REVISION"
        orden.save()
        return super().form_valid(form)


class FacturaListView(LoginRequiredMixin, CustomUserOnlyMixin, ListView):
    """
    Permite listar facturas
    **Context**

    ``Factura``
        An instance of :model:`store.Factura`.

    **Template:**

    :template:`factura/index.html`
    """
    model = Factura
    template_name = 'factura/index.html'
    context_object_name = 'facturas'
    paginate_by = 20
    queryset = Factura.objects.all()
    permissions_required = ('view_factura',)

    def get_queryset(self):
        new_context = self.queryset
        if self.request.GET.get('filter'):
            new_context = new_context.filter(Q(
                cliente__apellido__icontains=self.request.GET.get('filter')) | Q(
                cliente__nombre__icontains=self.request.GET.get('filter')) | Q(
                cliente__numero_identificacion__icontains=self.request.GET.get('filter')))

        return new_context

    def get_context_data(self, **kwargs):
        context = super(FacturaListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get(
            'filter') if self.request.GET.get('filter') else ''
        return context


class FacturaDetailView(LoginRequiredMixin, CustomUserOnlyMixin, DetailView):
    model = Factura
    permissions_required = ('view_factura',)
    template_name = 'factura/print.html'

    def get_context_data(self, **kwargs):
        context = super(FacturaDetailView, self).get_context_data(**kwargs)
        context['title'] = "Factura"
        context['asunto'] = "Factura"
        context['fecha'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return context


class FacturaDownloadView(WeasyTemplateResponseMixin, FacturaDetailView):
    pdf_filename = 'factura.pdf'


class FacturaCreateView(SuccessMessageMixin, LoginRequiredMixin, CustomUserOnlyMixin, CreateView):
    """
    Permite crear facturas
    **Context**

    ``Factura``
        An instance of :model:`store.Factura`.

    **Template:**

    :template:`factura/edit.html`
    """
    model = Factura
    form_class = FacturaForm
    template_name = 'factura/edit.html'
    success_message = 'Factura creada con exito'
    permissions_required = ('add_factura',)

    def form_valid(self, form):
        empresa = Empresa.objects.first()
        if empresa is None:
            raise ValidationError("Debe agregar datos de empresa")
        form.instance.empresa_id = empresa.id
        form.instance.estado = "POR_PAGAR"
        return super().form_valid(form)


class FacturaUpdateView(SuccessMessageMixin, LoginRequiredMixin, CustomUserOnlyMixin, UpdateView):
    """
    Permite editar facturas
    **Context**

    ``Factura``
        An instance of :model:`store.Factura`.

    **Template:**

    :template:`factura/edit.html`
    """
    model = Factura
    form_class = FacturaForm
    template_name = 'factura/edit.html'
    success_message = 'Factura actualizada con exito'
    permissions_required = ('change_factura',)

    def form_valid(self, form):
        empresa = Empresa.objects.first()
        if empresa is None:
            raise ValidationError("Debe agregar datos de empresa")
        form.instance.empresa_id = empresa.id
        form.instance.calcular_subtotal()
        form.instance.calcular_impuesto()
        form.instance.calcular_total()
        return super().form_valid(form)


class FacturaDeleteView(DeleteView, LoginRequiredMixin, CustomUserOnlyMixin):
    """
    Permite eliminar facturas
    **Context**

    ``Factura``
        An instance of :model:`store.Factura`.

    **Template:**

    :template:`delete.html`
    """
    model = Factura
    template_name = 'delete.html'
    success_url = reverse_lazy('invoices')
    permissions_required = ('delete_factura',)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('invoices')
            return HttpResponseRedirect(url)
        else:
            return super(FacturaDeleteView, self).post(request, *args, **kwargs)


class OrdenClienteListView(LoginRequiredMixin, CustomUserOnlyMixin, ListView):
    """
    Permite listar las órdenes de mantenimiento por cliente
    **Context**

    ``OrdenMantenimiento``
        An instance of :model:`store.OrdenMantenimiento`.

    **Template:**

    :template:`cliente/ordenMantenimiento/index.html`
    """
    model = OrdenMantenimiento
    template_name = 'cliente/ordenMantenimiento/index.html'
    context_object_name = 'ordenes'
    paginate_by = 20
    queryset = OrdenMantenimiento.objects.all()
    permissions_required = ('view_ordenmantenimiento',)

    def get_queryset(self):
        new_context = self.queryset.filter(
            cliente__id=self.request.user.persona_id)
        if self.request.GET.get('filter'):
            new_context = new_context.filter(
                Q(descripcion__icontains=self.request.GET.get('filter')) | Q(
                    cliente__apellido__icontains=self.request.GET.get('filter')) | Q(
                        cliente__nombre__icontains=self.request.GET.get('filter')) | Q(
                        cliente__numero_identificacion__icontains=self.request.GET.get('filter')))

        return new_context

    def get_context_data(self, **kwargs):
        context = super(OrdenClienteListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get(
            'filter') if self.request.GET.get('filter') else ''
        return context


class OrdenClienteDetailView(LoginRequiredMixin, CustomUserOnlyMixin, DetailView):
    model = OrdenMantenimiento
    permissions_required = ('view_ordenmantenimiento',)
    template_name = 'cliente/ordenMantenimiento/detail.html'


class DetalleFacturaListView(LoginRequiredMixin, CustomUserOnlyMixin, ListView):
    """
    Permite listar detalles de facturas
    **Context**

    ``DetalleFactura``
        An instance of :model:`store.DetalleFactura`.

    **Template:**

    :template:`detalleFactura/index.html`
    """
    model = DetalleFactura
    template_name = 'detalleFactura/index.html'
    context_object_name = 'detalles'
    paginate_by = 10
    queryset = DetalleFactura.objects.all()
    permissions_required = ('view_detalleFactura',)

    def get_queryset(self):
        new_context = self.queryset.filter(
            factura__id=self.kwargs['invoice_id'])
        if self.request.GET.get('filter'):
            new_context = new_context.filter(
                Q(detale=self.request.GET.get('filter')))

        return new_context

    def get_context_data(self, **kwargs):
        context = super(DetalleFacturaListView,
                        self).get_context_data(**kwargs)
        context['invoice_id'] = self.kwargs['invoice_id']
        context['filter'] = self.request.GET.get(
            'filter') if self.request.GET.get('filter') else ''
        return context


class DetalleFacturaCreateView(SuccessMessageMixin, CustomUserOnlyMixin, LoginRequiredMixin, CreateView):
    model = DetalleFactura
    form_class = DetalleFacturaForm
    template_name = 'detalleFactura/edit.html'
    success_message = 'Detalle creado con exito'
    permissions_required = ('add_detalleFactura',)

    def get_success_url(self):
        return reverse('invoice-detail-update', kwargs={'invoice_id': self.kwargs['invoice_id'], 'pk': self.object.pk, })

    def get_context_data(self, **kwargs):
        context = super(DetalleFacturaCreateView,
                        self).get_context_data(**kwargs)
        context['invoice_id'] = self.kwargs['invoice_id']
        return context

    def form_valid(self, form):
        factura = Factura.objects.get(id=self.kwargs['invoice_id'])
        form.instance.factura_id = factura.id
        form.instance.detalle = form.instance.producto.nombre
        producto = Producto.objects.get(id=form.instance.producto.id)
        producto.calcular_cantidad()
        if producto.cantidad <= 0:
            raise ValidationError("No ha stock del producto")
        producto.save()
        form.instance.calcular_total()
        form.save()
        factura.calcular_subtotal()
        factura.calcular_impuesto()
        factura.calcular_total()
        factura.save()
        return super().form_valid(form)


class DetalleFacturaUpdateView(SuccessMessageMixin, CustomUserOnlyMixin, LoginRequiredMixin, UpdateView):
    model = DetalleFactura
    form_class = DetalleFacturaForm
    template_name = 'detalleFactura/edit.html'
    success_message = 'Detalle actualizado con exito'
    permissions_required = ('change_detalleFactura',)

    def get_success_url(self, **kwargs):
        return reverse_lazy('invoice-details', kwargs={'invoice_id': self.kwargs['invoice_id']})

    def get_context_data(self, **kwargs):
        context = super(DetalleFacturaUpdateView,
                        self).get_context_data(**kwargs)
        context['invoice_id'] = self.kwargs['invoice_id']
        context['invoice_detail_id'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        producto = Producto.objects.get(id=form.instance.producto.id)
        producto.calcular_cantidad()
        if producto.cantidad <= 0:
            raise ValidationError("No ha stock del producto")
        producto.save()
        form.instance.calcular_total()
        form.save()
        factura = Factura.objects.get(id=self.kwargs['invoice_id'])
        factura.calcular_subtotal()
        factura.calcular_impuesto()
        factura.calcular_total()
        return super().form_valid(form)


class DetalleFacturaDeleteView(DeleteView, CustomUserOnlyMixin, LoginRequiredMixin):
    model = DetalleFactura
    template_name = 'delete.html'
    permissions_required = ('delete_detalleFactura',)

    def get_context_data(self, **kwargs):
        context = super(DetalleFacturaDeleteView,
                        self).get_context_data(**kwargs)
        context['invoice_id'] = self.kwargs['invoice_id']
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('invoice-details', kwargs={'invoice_id': self.kwargs['invoice_id']})

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy(
                'invoice-details',  kwargs={'invoice_id': self.kwargs['invoice_id']})
            return HttpResponseRedirect(url)
        else:
            detalle = DetalleFactura.objects.get(id=self.kwargs['pk'])
            producto = Producto.objects.get(id=detalle.producto.id)
            producto.calcular_cantidad()
            producto.cantidad = producto.cantidad + detalle.cantidad

            producto.save()
            factura = Factura.objects.get(id=self.kwargs['invoice_id'])
            factura.subtotal = factura.subtotal - detalle.total
            factura.calcular_impuesto()
            factura.calcular_total()
            factura.save()
            return super(DetalleFacturaDeleteView, self).post(request, *args, **kwargs)


class PagoFacturaListView(LoginRequiredMixin, CustomUserOnlyMixin, ListView):
    """
    Permite listar pagos de facturas
    **Context**

    ``PagoFactura``
        An instance of :model:`store.PagoFactura`.

    **Template:**

    :template:`pagoFactura/index.html`
    """
    model = PagoFactura
    template_name = 'pagoFactura/index.html'
    context_object_name = 'pagos'
    paginate_by = 10
    queryset = PagoFactura.objects.all()
    permissions_required = ('view_pagoFactura',)

    def get_queryset(self):
        new_context = self.queryset.filter(
            factura__id=self.kwargs['invoice_id'])
        if self.request.GET.get('filter'):
            new_context = new_context.filter(
                Q(detale=self.request.GET.get('filter')))

        return new_context

    def get_context_data(self, **kwargs):
        context = super(PagoFacturaListView,
                        self).get_context_data(**kwargs)
        context['invoice_id'] = self.kwargs['invoice_id']
        context['filter'] = self.request.GET.get(
            'filter') if self.request.GET.get('filter') else ''
        return context


class PagoFacturaCreateView(SuccessMessageMixin, CustomUserOnlyMixin, LoginRequiredMixin, CreateView):
    model = PagoFactura
    form_class = PagoFacturaForm
    template_name = 'pagoFactura/edit.html'
    success_message = 'Pago creado con exito'
    permissions_required = ('add_detalleFactura',)

    def get_success_url(self):
        return reverse('invoice-payment-update', kwargs={'invoice_id': self.kwargs['invoice_id'], 'pk': self.object.pk, })

    def get_context_data(self, **kwargs):
        context = super(PagoFacturaCreateView,
                        self).get_context_data(**kwargs)
        context['invoice_id'] = self.kwargs['invoice_id']
        return context

    def form_valid(self, form):
        factura = Factura.objects.get(id=self.kwargs['invoice_id'])
        form.instance.factura_id = factura.id
        form.save()
        factura.calcular_pagos()
        factura.save()
        return super().form_valid(form)


class PagoFacturaUpdateView(SuccessMessageMixin, CustomUserOnlyMixin, LoginRequiredMixin, UpdateView):
    model = PagoFactura
    form_class = PagoFacturaForm
    template_name = 'pagoFactura/edit.html'
    success_message = 'Pago actualizada con exito'
    permissions_required = ('change_pagoFactura',)

    def get_success_url(self, **kwargs):
        return reverse_lazy('invoice-payments', kwargs={'invoice_id': self.kwargs['invoice_id']})

    def get_context_data(self, **kwargs):
        context = super(PagoFacturaUpdateView,
                        self).get_context_data(**kwargs)
        context['invoice_id'] = self.kwargs['invoice_id']
        context['invoice_payment_id'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        form.save()
        factura = Factura.objects.get(id=self.kwargs['invoice_id'])
        factura.calcular_pagos()
        factura.save()
        return super().form_valid(form)


class PagoFacturaDeleteView(DeleteView, CustomUserOnlyMixin, LoginRequiredMixin):
    model = PagoFactura
    template_name = 'delete.html'
    permissions_required = ('delete_pagoFactura',)

    def get_context_data(self, **kwargs):
        context = super(PagoFacturaDeleteView,
                        self).get_context_data(**kwargs)
        context['invoice_id'] = self.kwargs['invoice_id']
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('invoice-payments', kwargs={'invoice_id': self.kwargs['invoice_id']})

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy(
                'invoice-payments',  kwargs={'invoice_id': self.kwargs['invoice_id']})
            return HttpResponseRedirect(url)
        else:
            pago = PagoFactura.objects.get(id=self.kwargs['pk'])

            factura = Factura.objects.get(id=self.kwargs['invoice_id'])
            factura.calcular_pagos() - pago.monto
            factura.save()
            return super(PagoFacturaDeleteView, self).post(request, *args, **kwargs)


class PagoFacturaDetailView(LoginRequiredMixin, CustomUserOnlyMixin, DetailView):
    model = PagoFactura
    permissions_required = ('view_pagofactura',)
    template_name = 'pagoFactura/print.html'

    def get_context_data(self, **kwargs):
        context = super(PagoFacturaDetailView, self).get_context_data(**kwargs)
        context['title'] = "Pago"
        context['asunto'] = "Pago"
        context['fecha'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return context


class PagoFacturaDetailViewDownloadView(WeasyTemplateResponseMixin, PagoFacturaDetailView):
    pdf_filename = 'pago.pdf'
