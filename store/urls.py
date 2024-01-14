from pprint import pprint
from django.urls import path
from . import views
from rest_framework_nested import routers

# Parent routers
router = routers.DefaultRouter()  # with this we can hit http://127.0.0.1:8000/store
# router = SimpleRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
# pprint(router.urls)  # This contains url patterns, will generate 4 endpoint as defined below.

# Child routers
# lookup='product' means we will have parameter product_pk in our route
product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
# register child resource
product_router.register('reviews', views.ReviewViewSet, basename='product-reviews')


urlpatterns = router.urls + product_router.urls

# urlpatterns = [
#     path('', include(router.urls)),
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view()),
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail')
# ]