from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ordenes/$', views.index, name='ordenes'),
      url(r'^ordenes/edit/(\d+)$', views.editar_orden, name='editar-orden'),
]
