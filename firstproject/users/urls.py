from .import views
from django.urls import path

urlpatterns = [
    path('login/', views.login_api),
    path('users/', views.get_user_data),
]