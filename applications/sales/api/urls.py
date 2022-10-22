from rest_framework import routers
from .views import OrderView, OrderDetailView, OrderGainView, ClientViewSet, OrdersOfClientView, ProductViewSet
from django.urls import path
from django.conf.urls import include

router = routers.DefaultRouter()
router.register('client', ClientViewSet)
router.register('product', ProductViewSet)

urlpatterns = [
    path('', include(router.urls), name='api-sales-client'),
    path('order/', OrderView.as_view(), name='api-sales-order'),
    path('order-detail/<int:id>/', OrderDetailView.as_view(), name='api-sales-order-detail'),
    path('order-gain/<int:id>/', OrderGainView.as_view(), name='api-sales-order-gain'),
    path('orders-client/<int:id>/', OrdersOfClientView.as_view(), name='api-sales-orders-client'),
]