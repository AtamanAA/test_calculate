from django.urls import path
from . import views
from .views import PasswordsChangeView


urlpatterns = [    
    path('login_user/', views.login_user, name = 'login'),
    path('logout_user/', views.logout_user, name = 'logout'),
    path('register_user/', views.register_user, name = 'register'),
    path('update_user/', views.update_user, name = 'update_user'),
    path('change_password/', PasswordsChangeView.as_view(), name = 'change_password'),
]