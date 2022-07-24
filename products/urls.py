from django.urls import path
from . import views  # to import views from .py needed to display urls


'''remeber to include app urls in the project level url file'''


urlpatterns = [
    path('', views.all_products, name='products'),  # all_products is from the views, name is product (product being viewed?)
    path('<product_id>', views.product_detail, name='product_detail'),  # <product_id> is pased from db to show in url
]