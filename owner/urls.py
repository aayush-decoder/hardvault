from django.contrib import admin
from django.urls import path
from . import views

# Owner

urlpatterns = [
    path('login/', views.login, name="client-login"),
    path('data/api/', views.receive_data, name="receive-data")
]
