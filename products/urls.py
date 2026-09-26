from django.urls import path

from . import views


urlpatterns = [
    # Products
    path('product/', views.product_list, name='product_list'),
    path(
        'products/<int:id>/',
        views.product_detail,
        name='product_detail',
    ),

    # Cart
    path('cart/', views.cart, name='cart'),
    path(
        'cart/add/<int:id>/',
        views.add_to_cart,
        name='add_to_cart',
    ),
    path(
        'cart/increase/<int:id>/',
        views.increase_quantity,
        name='increase_quantity',
    ),
    path(
        'cart/decrease/<int:id>/',
        views.decrease_quantity,
        name='decrease_quantity',
    ),
    path(
        'cart/remove/<int:id>/',
        views.remove_from_cart,
        name='remove_from_cart',
    ),
]