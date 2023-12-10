from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models


# Register your models here.
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    # Reduces number of query by preloading
    # because we are doing product.collection.title
    list_select_related = ['collection']
    search_fields = ['title']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    def collection_title(self, product):
        return product.collection.title


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'order_count']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', ]

    # ADD A COLUMN TO VIEW ORDER OF EACH CUSTOMER (LINK)
    @admin.display(ordering='order_count')
    def order_count(self, customer):
        # reverse('admin:app_model_page')  Django function that gives the URL of page in admin interface (See syntax)
        url = (
                reverse('admin:store_order_changelist')
                + '?'
                + urlencode({'customer__id': str(customer.id)})
        )
        return format_html('<a href={}>{}</a>', url, customer.order_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            order_count=Count('order')
        )


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    model = models.OrderItem
    extra = 0  # Don't show extra rows while adding new product to order


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    list_per_page = 10
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]


# By registering model to admin we can access it from admin interface
# admin.site.register(models.Collection)
#  admin.site.register(models.Product)


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        # reverse('admin:app_model_page')  Django function that gives the URL of page in admin interface (See syntax)
        url = (
                reverse('admin:store_product_changelist')
                + '?'
                + urlencode({'collection__id': str(collection.id)})
            # attach query string to the url to filter product page for that collection only
        )
        return format_html('<a href={}>{}</a>', url, collection.product_count)
        # return collection.product_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count=Count('product')
        )
