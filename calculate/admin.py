from django.contrib import admin
from .models import Material, PipeHighPressure


class MaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "condition", "hardness", "yield_strenght")


class PipeHighPressureAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "description", "yield_strength", "test_pressure", "min_outside_diameter", "k_industry", "k_cycle", "k_welding", "thickness", "created_at")

    # fieldsets = (    
    #     ('General info', {
    #         'fields': [('user', 'name', 'description')]
    #     }),
    #     ('Calculate properties', {
    #         'fields': [('yield_strength', 'test_pressure', 'k_industry', 'k_cycle', 'k_welding')]
    #     }),
    #     ('Geometry', {
    #         'fields': [('min_outside_diameter', 'pipe_thickness')]
    #     }),
    # )

admin.site.register(Material, MaterialAdmin)
admin.site.register(PipeHighPressure, PipeHighPressureAdmin)
