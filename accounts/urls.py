from django.urls import path
from . import views

urlpatterns = [
    # Registration
    path('owner/register/', views.owner_register, name='owner-register'),
    
    # Login/Logout
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Password Reset
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('verify-reset-otp/', views.verify_reset_otp, name='verify-reset-otp'),
    path('reset-password/', views.reset_password, name='reset-password'),
    
    # Dashboards
    path('owner/dashboard/', views.owner_dashboard, name='owner-dashboard'),
    
    # API
    path('api/search-owners/', views.search_owners, name='search-owners'),
    path('api/resend-otp/', views.resend_otp, name='resend-otp'),
]
