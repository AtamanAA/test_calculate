from django.urls import path
from . import views

urlpatterns = [
    path("", views.instructions, name="instructions_index"),
    path("pipe_pressure", views.pipe_pressure, name="pipe_pressure_instruction"),
    path("pipe_pressure_assembly", views.pipe_pressure_assembly, name="pipe_pressure_assembly_instruction"),
]