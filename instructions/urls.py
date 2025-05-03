from django.urls import path
from . import views

urlpatterns = [
    path("instructions/", views.instructions, name="instructions_index"),
    path("instructions/pipe_pressure", views.pipe_pressure, name="pipe_pressure_instruction"),
]