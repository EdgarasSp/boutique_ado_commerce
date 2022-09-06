from decimal import Decimal   ## decimal function used in delivery calc. 
                              #NOTE: use decimal for financial calculations due to rounding
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):

    bag_items = []  ## variable to save items into
    total = 0        ## set default value to update afer
    product_count = 0  ## set default value to update afer
    bag = request.session.get('bag', {})  ## gets bag from context session if does not exist creates new

    ### calculates bag total and creates product dictionary which will be used for creating shopping bag items view
    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)  # imported products to get ID's
        total += quantity * product.price
        product_count += quantity
        bag_items.append({   # library to get product details
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)    # settings means from settings.py het variable STANDARD_DELIVERY_PERCENTAGE. total divided by % set
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total
    
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context  # this context processor made available to 
                    #all templates, need to ad to settings.py "templates" "Context processor" 