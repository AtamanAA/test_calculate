from django.contrib import admin
from .models import Material


class MaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "condition", "hardness", "yield_strenght")
    # list_display_links = ("name",)
    # fields = [("name", "surname"), "patronymic", "books"]

admin.site.register(Material, MaterialAdmin)