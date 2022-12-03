from django.contrib import admin
from .models import inventory,items

# Register your models here.
admin.site.register(inventory)
admin.site.register(items)