# Register your models here.

from django.contrib import admin
from . import models


# Register your models here.


class MenuInline(admin.TabularInline):
    model = models.Menu


class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Bakery)
class BakeryAdmin(admin.ModelAdmin):
    inlines = (
        MenuInline,
        PhotoInline,
    )


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Menu)
class MenuAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

