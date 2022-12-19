from django.urls import path

from . import views

urlpatterns = [	
	path('', views.index, name = 'index'),
	path('pipe_pressure/', views.pipe_pressure, name = 'pipe_pressure'),
	path('thread/', views.thread, name = 'thread'),
	path('materials/', views.materials, name = 'materials'),
]