from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer


# Create your views here.


@api_view(['GET', 'POST'])
def product_list(request):
    """
    Handle requests like
    localhost:3000/store/products/
    :param request:
    :return:
    Sample payload for creating a product
    {
        "title": "7up Diet, 355 Ml",
        "description": "suspendisse",
        "slug": "-",
        "inventory": 0,
        "unit_price": 79.07,
        "collection": 5
    }
    """
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)  # This deserializes the data
        # Data from client has to be validated before accessing
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # print(serializer.validated_data)
        # For extra validation apart from that is done at model validation level from is_valid method,
        # we can override it.

        return Response("OK")


@api_view()
def product_detail(request, id):
    """
    Handle requests like
    localhost:3000/store/products/1/
    :param request:
    :param id:
    :return:
    """
    try:
        product = Product.objects.get(pk=id)
        # Moment we create below serializer object it converts product object to dictionary
        serializer = ProductSerializer(product)
        # Then behind the scene django will convert dictionary to json object and will be returned.
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # ************* #
    # product = get_object_or_404(Product, pk=id)
    # serializer = ProductSerializer(product)
    # return Response(serializer.data)


@api_view()
def collection_detail(request, pk):
    return Response("ok")
