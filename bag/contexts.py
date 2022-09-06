from decimal import Decimal   ## decimal function used in delivery calc. 
                              #NOTE: use decimal for financial calculations due to rounding
from django.conf import settings

def bag_contents(request):

    bag_items = []  ## variable to save items into
    total = 0        ## set default value to update afer
    product_count = 0  ## set default value to update afer

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