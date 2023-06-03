from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("pipe_pressure/", views.pipe_pressure, name="pipe_pressure"),
    path("pipe_pressure/results/", views.pipe_results, name="pipe_results"),
    path("pipe_pressure/detail/", views.pipe_detail, name="pipe_detail"),
    path("thread/", views.thread, name="thread"),
    path("thread/results/", views.thread_results, name="thread_results"),
    path("thread/detail/", views.thread_detail, name="thread_detail"),
    path("materials/", views.materials, name="materials"),
]
