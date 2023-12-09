from django.contrib import admin
from . import models

# Register your models here.

# By registering model to admin we can access it from admin interface
admin.site.register(models.Collection)
admin.site.register(models.Product)