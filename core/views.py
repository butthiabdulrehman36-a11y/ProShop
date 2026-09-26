from django.shortcuts import render

from products.models import Product


def home(request):
    """
    Display the ProShop home page with all products.
    """

    products = Product.objects.all()

    return render(
        request,
        'core/home.html',
        {'products': products},
    )