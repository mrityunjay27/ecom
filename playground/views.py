from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, OrderItem
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F


# Create your views here.
def say_hello(request):
    x = 1
    y = 2
    z = x + y
    # Django converts Orm code to sql code at run time
    # Migrations are also part of Django ORM
    # Product.objects => return a Manager Object, which as functions to interact with DB
    # query_set = Product.objects.all()
    # Query sets are lazy they are not evaluated instantly, as we can have complex query sets (By chaining),
    # so it's better to evaluate at once. It gets evaluated when
    # 1. We iterate
    #       for product in query_set:
    #           print(product)
    # 2. Convert to list
    #       list(query_set)
    # 3. Index or slice query_set[0:3]

    # Some methods of Manager return result instantly count(), get()

    try:
        product = Product.objects.get(pk=1)
    except ObjectDoesNotExist:
        print("Object not found")

    product = Product.objects.filter(pk=0).first()
    # Query set return empty, first() return None.

    exists = Product.objects.filter(pk=0).exists()
    # exists return boolean.

    # Field Lookups
    qs1 = Product.objects.filter(unit_price__gt=20)
    qs2 = Product.objects.filter(unit_price__range=(20, 30))
    qs3 = Product.objects.filter(collection__id__range=(1, 3))
    qs4 = Product.objects.filter(title__icontains="coffee")
    qs5 = Product.objects.filter(last_update__year=2021)
    qs6 = Product.objects.filter(description__isnull=True)

    # Complex QuerySet
    # qs7 and qs8 are same (and)
    qs7 = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    qs8 = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)

    # OR |, ~, &
    qs8 = Product.objects.filter(Q(inventory__lt=10) | ~Q(unit_price__lt=20))

    # F class is used to reference particular field in model
    # Get product where inventory = unit_price
    qs9 = Product.objects.filter(inventory=F('unit_price'))
    # also work for referencing related table's fields
    qs10 = Product.objects.filter(inventory=F('collection__id'))

    # Sorting data
    qs11 = Product.objects.order_by('unit_price', '-title')
    # p1 is same as p2
    p1 = Product.objects.order_by('unit_price')[0]
    p2 = Product.objects.earliest('unit_price')  # ASC
    p3 = Product.objects.latest('unit_price')  # DSC

    # Limiting results
    qs12 = Product.objects.all()[:5]  # 0 1 2 3 4
    qs13 = Product.objects.all()[5:10]  # 5 6 7 8 9

    # Reading subset of fields in the table
    # Returns all the product's id and title and collection's title
    # This return a list of Dictionary Ex. {'id': 2, 'title': 'Apple', 'collection__title': 'Fruits'}  }
    qs14 = Product.objects.values('id', 'title', 'collection__title')
    # This returns list of tuples Ex. (2, 'Apple', 'Fruits')
    qs15 = Product.objects.values_list('id', 'title', 'collection__title')

    # Ques: Select products that have been ordered ad sort them by title
    # This product_id field will automatically be generated at run time.
    qs_order_items = OrderItem.objects.values('product_id').distinct()
    qs_product = Product.objects.filter(id__in=qs_order_items).order_by('title')

    return render(request, 'hello.html', {'name': 'Rambo', 'products': list(qs_product)})
