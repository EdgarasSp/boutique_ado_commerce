from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages  # FOR REPORTING ERROR MESSAGES LINE 18
from django.db.models import Q # USED TO GENERATE A SEARCH QUERY, THIS USED TO GET 'OR OPTION/I.E SEARCH WORD IN DESCRIPTION OR PRODUCT NAME, WITHOUT IT WORD MUST BE PRESENT IN BOTH TO BE MATCH
from .models import Product, Category  # imports our Products database, cat used to show user cats filtered to
from django.db.models.functions import Lower # this somehow fixes sort by name error due to appended 'lowe'_name 
from .forms import ProductForm
# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()  # imports all our products from the database
    query = None # SET VARIABLE DEFAULT
    categories = None # SET VARIABLE DEFAULT
    sort = None # note that default needed to be specified so that teplates load works when variable not used
    direction = None

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


        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name': # is sort key is equil to name
                sortkey = 'lower_name' # temp field, lower_name
                products = products.annotate(lower_name=Lower('name')) # products model, add (annotate) colm (lower_name) to be (.LOWER) passing 'name' field
                # annotate means add a temporary field on the model

            if sortkey == 'category':
                sortkey = 'category__name' # this double __ something like adding category and sorting data to sortkey variable

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':  # if desending
                    sortkey = f'-{sortkey}' # add - to change sorting
            products = products.order_by(sortkey)  # products db update sort key
            
    current_sorting = f'{sort}_{direction}' # this returns to the template, fields from main nav sort ca
    # this one is used by products.html passes value from in page sorting?

    context = {
        'products': products,  #add the products to the context so that it could be added to the template
        'search_term': query,  # query word will show in url as q=jeans
        'current_categories': categories, # rxytacted to show current filtred categories
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)  # first 'products/products.html is where html template located, then context is to send things back to the template?


def product_detail(request, product_id):  # product id is what item is requested
    """ A view to show a product, including sorting and search queries """

    product = get_object_or_404(Product, pk=product_id)  # imports a product from the database asper passed parameter 'product_id'

    context = {
        'product': product,  #add the product to the context so that it could be added to the template
    }

    return render(request, 'products/product_detail.html', context)  # first 'products/products.html is where html template located, then context is to send things back to the template?


def add_product(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def edit_product(request, product_id):
    """ Edit a product in the store """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


def delete_product(request, product_id):
    """ Delete a product from the store """
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))