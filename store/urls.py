from django.urls import path

from store.views import OrdenCreateView, OrdenListView, OrdenDeleteView, OrdenUpdateView

urlpatterns = [
    path('orders', OrdenListView.as_view(), name='orders'),
    path('orders/add/', OrdenCreateView.as_view(), name='order-add'),
    path('orders/<int:pk>/', OrdenUpdateView.as_view(), name='order-update'),
    path('orders/<int:pk>/delete/', OrdenDeleteView.as_view(), name='order-delete'),
]
