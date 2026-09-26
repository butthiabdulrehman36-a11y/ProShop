from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product

from .forms import OrderForm
from .models import Order, OrderItem


@login_required(login_url='/login/')
def checkout(request):
    """
    Create a new order from the current user's session cart.
    """

    cart = request.session.get('cart', {})

    # Do not allow checkout with an empty cart.
    if not cart:
        return redirect('cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)

                # Attach the logged-in user to the order.
                order.user = request.user

                total_amount = 0
                products = []

                # Validate stock and calculate the order total.
                for product_id, quantity in cart.items():
                    product = get_object_or_404(
                        Product,
                        id=product_id,
                    )

                    if product.stock < quantity:
                        return render(
                            request,
                            'orders/checkout.html',
                            {
                                'form': form,
                                'error': (
                                    f'{product.name} has only '
                                    f'{product.stock} items available.'
                                ),
                            },
                        )

                    total_amount += product.price * quantity
                    products.append(
                        (product, quantity)
                    )

                order.total_amount = total_amount
                order.save()

                # Create order items and reduce product stock.
                for product, quantity in products:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price,
                    )

                    product.stock -= quantity

                    product.save(
                        update_fields=['stock']
                    )

            # Clear the cart only after a successful order.
            request.session['cart'] = {}
            request.session.modified = True

            return redirect(
                'order_success',
                order_id=order.id,
            )

    else:
        form = OrderForm()

    return render(
        request,
        'orders/checkout.html',
        {'form': form},
    )


@login_required(login_url='/login/')
def order_success(request, order_id):
    """
    Display the success page for the logged-in user's order.
    """

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    return render(
        request,
        'orders/order_success.html',
        {'order': order},
    )


@login_required(login_url='/login/')
def order_detail(request, order_id):
    """
    Display details of an order owned by the logged-in user.
    """

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    return render(
        request,
        'orders/order_detail.html',
        {'order': order},
    )


@login_required(login_url='/login/')
def order_history(request):
    """
    Display the logged-in user's orders, newest first.
    """

    orders = Order.objects.filter(
        user=request.user,
    ).order_by('-created_at')

    return render(
        request,
        'orders/order_history.html',
        {'orders': orders},
    )