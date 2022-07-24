from django.shortcuts import render, get_object_or_404
from .models import Product  # imports our Products database

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()  # imports all our products from the database

    context = {
        'products': products,  #add the products to the context so that it could be added to the template
    }

    return render(request, 'products/products.html', context)  # first 'products/products.html is where html template located, then context is to send things back to the template?


def product_detail(request, product_id):  # product id is what item is requested
    """ A view to show a product, including sorting and search queries """

    product = get_object_or_404(Product, pk=product_id)  # imports a product from the database asper passed parameter 'product_id'

    context = {
        'product': product,  #add the product to the context so that it could be added to the template
    }

    return render(request, 'products/product_detail.html', context)  # first 'products/products.html is where html template located, then context is to send things back to the template?