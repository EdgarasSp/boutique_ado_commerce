from django.contrib import admin
from .models import Product, Category

# Register your models here.


class ProductAdmin(admin.ModelAdmin):  # SETUPS WHICH COLUMNS TO SHOW IN ADMIN
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)  # SET TO ORDERING NOTE MUST BE A TUPLE I.E IF ONE HAS TO HAVE A COMMA, TO REVERS AD - I.E '-sku'
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Product, ProductAdmin) # here register models i.e 'Product" and classes i.e 'ProductAdmin'
admin.site.register(Category, CategoryAdmin)