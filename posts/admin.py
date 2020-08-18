from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Bakery_post)
class BakeryPostAdmin(admin.ModelAdmin):
    pass