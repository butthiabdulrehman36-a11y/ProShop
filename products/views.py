from django.shortcuts import get_object_or_404, redirect, render

from .models import Product


def product_list(request):
    """
    Display all available products.
    """

    products = Product.objects.all()

    return render(
        request,
        'Products/product_list.html',
        {'products': products},
    )


def product_detail(request, id):
    """
    Display details for a single product.
    """

    product = get_object_or_404(
        Product,
        id=id,
    )

    return render(
        request,
        'Products/product_detail.html',
        {'product': product},
    )


def add_to_cart(request, id):
    """
    Add one unit of a product to the session cart.
    """

    product = get_object_or_404(
        Product,
        id=id,
    )

    # Do not allow out-of-stock products.
    if product.stock <= 0:
        return redirect(
            'product_detail',
            id=product.id,
        )

    cart = request.session.get('cart', {})
    product_id = str(product.id)

    current_quantity = cart.get(
        product_id,
        0,
    )

    # Do not allow quantity above available stock.
    if current_quantity >= product.stock:
        return redirect(
            'product_detail',
            id=product.id,
        )

    cart[product_id] = current_quantity + 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect(
        'product_detail',
        id=product.id,
    )


def increase_quantity(request, id):
    """
    Increase cart quantity without exceeding available stock.
    """

    cart = request.session.get('cart', {})
    product = get_object_or_404(
        Product,
        id=id,
    )

    product_id = str(id)

    if product_id in cart:
        if cart[product_id] < product.stock:
            cart[product_id] += 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def decrease_quantity(request, id):
    """
    Decrease cart quantity or remove the product at quantity one.
    """

    cart = request.session.get('cart', {})
    product_id = str(id)

    if product_id in cart:
        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def remove_from_cart(request, id):
    """
    Remove a product completely from the session cart.
    """

    cart = request.session.get('cart', {})
    product_id = str(id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def cart(request):
    """
    Display the current session cart.

    Products that no longer exist are removed safely.
    Quantities are also corrected when stock has decreased.
    """

    cart = request.session.get('cart', {})
    products = []
    cleaned_cart = {}

    for product_id, quantity in cart.items():

        try:
            product = Product.objects.get(
                id=product_id,
            )
        except Product.DoesNotExist:
            continue

        # Remove products that are completely out of stock.
        if product.stock <= 0:
            continue

        # Never allow cart quantity above current stock.
        quantity = min(
            quantity,
            product.stock,
        )

        cleaned_cart[product_id] = quantity

        products.append({
            'product': product,
            'quantity': quantity,
        })

    request.session['cart'] = cleaned_cart
    request.session.modified = True

    return render(
        request,
        'Products/cart.html',
        {'products': products},
    )
