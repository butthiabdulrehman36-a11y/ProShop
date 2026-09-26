from django.urls import path

from . import views


urlpatterns = [
    # Checkout
    path(
        'checkout/',
        views.checkout,
        name='checkout',
    ),

    # Order Success
    path(
        'success/<int:order_id>/',
        views.order_success,
        name='order_success',
    ),

    # Order Detail
    path(
        'detail/<int:order_id>/',
        views.order_detail,
        name='order_detail',
    ),

    # Order History
    path(
        'history/',
        views.order_history,
        name='order_history',
    ),
]