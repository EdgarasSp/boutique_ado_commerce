from django.shortcuts import render
from .models import Product  # imports our Products database

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()  # imports all our products from the database

    context = {
        'products': products,  #add the products to the context so that it could be added to the template
    }

    return render(request, 'products/products.html', context)  # first 'products/products.html is where html template located, then context is to send things back to the template?