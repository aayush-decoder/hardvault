from django.contrib import admin
from django.urls import path
from . import views

# Client

urlpatterns = [
    path('login/', views.login, name="client-login"),
    path('form/', views.form, name="product-form"),
    path('form/download', views.download_file, name="download-file"),
]
