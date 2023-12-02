from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product
from django.core.exceptions import ObjectDoesNotExist


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

    return render(request, 'hello.html', {'name': 'Rambo'})
