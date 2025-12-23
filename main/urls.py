from django.urls import path

from main.views import CustomerViewSet, ShopViewSet, CartViewSet, ProductViewSet, CartItemViewSet

urlpatterns = [
    path("customer/", CustomerViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('shop/', ShopViewSet.as_view({'post': 'create'})),
    path('cart/', CartViewSet.as_view({'post': 'create'})),
    path('product/', ProductViewSet.as_view({'post': 'create'})),
    path('cart-item/', CartItemViewSet.as_view({'post': 'create'})),

    path('customer/<int:pk>/', CustomerViewSet.as_view(
        {
            'get': 'retrieve',
            'delete': 'destroy',
            'put': 'update',
            'patch': 'partial_update'
        }
    )),
    path('shop/<int:pk>/', ShopViewSet.as_view(
        {
            'get': 'retrieve',
            'delete': 'destroy',
            'put': 'update',
            'patch': 'partial_update'
        }
    )),
    path('cart/<int:pk>/', CartViewSet.as_view(
        {
            'get': 'retrieve',
            'delete': 'destroy',
            'put': 'update',
            'patch': 'partial_update'
        }
    )),
    path('product/<int:pk>/', ProductViewSet.as_view(
        {
            'get': 'retrieve',
            'delete': 'destroy',
            'put': 'update',
            'patch': 'partial_update'
        }
    )),
    path('cart-item/<int:pk>/', CartItemViewSet.as_view(
        {
            'get': 'retrieve',
            'delete': 'destroy',
            'put': 'update',
            'patch': 'partial_update'
        }
    ))
]
