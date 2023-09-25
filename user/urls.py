from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('dup-check/', views.dup_check, name="dup_check"),
    path('create/', views.create, name="create"),
    path('login/', views.login, name="login"),
    path('find-id/', views.find_id, name="find_id"),
    path('reset-password/', views.reset_password, name="reset_password"),
]