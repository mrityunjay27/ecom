from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.


@api_view()
def product_list(request):
    """
    Handle requests like
    localhost:3000/store/products/
    :param request:
    :return:
    """
    return Response("ok")


@api_view()
def product_detail(request, id):
    """
    Handle requests like
    localhost:3000/store/products/1/
    :param request:
    :param id:
    :return:
    """
    return Response(id)
