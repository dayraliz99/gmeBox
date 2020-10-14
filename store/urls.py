from django.urls import path

from store import views
urlpatterns = [
    path('orders', views.OrdenListView.as_view(), name='orders'),
    path('orders/add/', views.OrdenCreateView.as_view(), name='order-add'),
    path('orders/<int:pk>/', views.OrdenUpdateView.as_view(), name='order-update'),
    path('orders/<int:pk>/delete/', views.OrdenDeleteView.as_view(), name='order-delete'),
    path('clients', views.ClienteListView.as_view(), name='clients'),
    path('clients/add/',
         views.ClienteCreateView.as_view(), name='client-add'),
    path('clients/<int:pk>/',
         views.ClienteUpdateView.as_view(), name='client-update'),
    path('clients/<int:pk>/delete/',
         views.ClienteDeleteView.as_view(), name='client-delete'),
]
