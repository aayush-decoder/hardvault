from django.contrib import admin
from django.urls import path
from . import views

# Client

urlpatterns = [
    path('login/', views.login, name="client-login"),
    path('form/', views.form, name="product-form"),
    path('form/submit', views.submit_form, name="submit-form"),
    path('form/download', views.download_file, name="download-page"),
    path('form/download-exe', views.download_exe, name="download-exe-file"),
    path('data/api', views.fetch_data, name="client-data-api")
]
