from django.contrib import admin

# Register your models here.
from .models import Ready, ToBeProduced, Intransit, AtpStock, Sales

admin.site.register(Ready)
admin.site.register(ToBeProduced)
admin.site.register(Intransit)
admin.site.register(AtpStock)
admin.site.register(Sales)