from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages  # FOR REPORTING ERROR MESSAGES LINE 18
from django.db.models import Q # USED TO GENERATE A SEARCH QUERY, THIS USED TO GET 'OR OPTION/I.E SEARCH WORD IN DESCRIPTION OR PRODUCT NAME, WITHOUT IT WORD MUST BE PRESENT IN BOTH TO BE MATCH
from .models import Product, Category  # imports our Products database, cat used to show user cats filtered to

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()  # imports all our products from the database
    query = None # SET VARIABLE DEFAULT
    categories = None # SET VARIABLE DEFAULT

    if request.GET:  #IF THIS VIEW RECEIVES GET REQUEST FROM BASE/MOBILE NAV FORM line 60
        if 'q' in request.GET: # IF REQUEST RECEIVED US Q FOR QUERY AS VALUE SET IN BASE/MOBILE NAV FORM
            query = request.GET['q']  # SET VARIABLE TO Q, q is search term (not sure how its passed from the form)
            if not query:  # IF NO Q THEN ERROR MESSAGE
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query) # SEARCH TERM Q 'BLOUSE' CHECK NAME OR DESCRIPTION FOR MATCH NOTE '|' MEANS or. NOTE __i makes word case insesitive
            products = products.filter(queries)  # RESETS VARIABLE FROM ALL TO FILTERED RESULT

        if 'category' in request.GET: # coming from the main nav get from subdropdwons
            categories = request.GET['category'].split(',') # split on , delimiter if more than one listed and assign to vasriable
            products = products.filter(category__name__in=categories) # filter products with new variables
            categories = Category.objects.filter(name__in=categories) # used to capured filtered categories to show the user.

    context = {
        'products': products,  #add the products to the context so that it could be added to the template
        'search_term': query,  # query word will show in url as q=jeans
        'current_categories': categories, # rxytacted to show current filtred categories
    }

    return render(request, 'products/products.html', context)  # first 'products/products.html is where html template located, then context is to send things back to the template?


def product_detail(request, product_id):  # product id is what item is requested
    """ A view to show a product, including sorting and search queries """

    product = get_object_or_404(Product, pk=product_id)  # imports a product from the database asper passed parameter 'product_id'

    context = {
        'product': product,  #add the product to the context so that it could be added to the template
    }

    return render(request, 'products/product_detail.html', context)  # first 'products/products.html is where html template located, then context is to send things back to the template?