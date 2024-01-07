from django.contrib import admin, messages
from django.db.models import Count, QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from tags.models import TaggedItem
from . import models


#  Custom Filter
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'  # This will be part of query string

    def lookups(self, request, model_admin):
        return [
            # (value, string to display)
            ('<10', 'Low'),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # inlines = [TagInline]
    prepopulated_fields = {'slug': ['title']}  # Pre-populates slug field while adding product
    autocomplete_fields = ['collection']  # Auto-completed collection field while adding product
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    # Reduces number of query by preloading
    # because we are doing product.collection.title
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]
    search_fields = ['title']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    def collection_title(self, product):
        return product.collection.title

    #  Defining custom actions
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        """
        query set is the object the is selected to delete
        :param request:
        :param queryset:
        :return:
        """
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f'{updated_count} products were successfully updated', messages.ERROR)


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
    search_fields = ['title']

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
            product_count=Count('products')
        )
