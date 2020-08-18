
# Register your models here.

from django.contrib import admin
from . import models


# Register your models here.


@admin.register(models.Bakery)
class BakeryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Menu)
class MenuAdmin(admin.ModelAdmin):
    pass


