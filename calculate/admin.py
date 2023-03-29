from django.contrib import admin
from .models import Material, PipeHighPressure, ThreadConnection


class MaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "condition", "hardness", "yield_strenght")


class PipeHighPressureAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "description", "yield_strength", "test_pressure", "min_outside_diameter", "k_industry", "k_cycle", "k_welding", "thickness", "created_at")

class ThreadConnectionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "description", "axial_force", "bolt_yield_strength", "nut_yield_strength", "nominal_thread_diameter", "thread_pitch", "nut_active_height", "nut_minimum_diameter", "bolt_hole_diameter", "k_industry", "k_thread", "created_at", "k_bolt_tension", "k_nut_tension", "k_bolt_crush", "k_nut_crush", "k_bolt_shear", "k_nut_shear",)

admin.site.register(Material, MaterialAdmin)
admin.site.register(PipeHighPressure, PipeHighPressureAdmin)
admin.site.register(ThreadConnection, ThreadConnectionAdmin)
