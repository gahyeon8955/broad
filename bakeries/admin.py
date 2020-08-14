
# Register your models here.

from django.contrib import admin
from . import models


# Register your models here.


@admin.register(models.Bakery)
class BakeryAdmin(admin.ModelAdmin):
    pass
