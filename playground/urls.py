from django.urls import path
from . import views

# UrlConfig
urlpatterns = [
    path('hello/', views.say_hello)
]