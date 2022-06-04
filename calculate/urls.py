from django.urls import path

from . import views

urlpatterns = [
	# Домашняя страница
	path('', views.index, name = 'index'),
	path('pipe_pressure/', views.pipe_pressure, name = 'pipe_pressure'),
	path('thread/', views.thread, name = 'thread'),
	path('sandbox/', views.sandbox, name = 'sandbox'),
	path('sandbox/results/', views.sandbox_results, name = 'sandbox_results'),
]