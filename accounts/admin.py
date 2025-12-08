from django.contrib import admin
from .models import User, Owner, Client, OTP

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'user_type', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name']

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'invitation_code']
    search_fields = ['company_name', 'user__email']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_owners']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    
    def get_owners(self, obj):
        return ", ".join([owner.company_name for owner in obj.owners.all()])
    get_owners.short_description = 'Owners'

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['email', 'otp_code', 'otp_type', 'created_at', 'expires_at', 'is_verified']
    list_filter = ['otp_type', 'is_verified']
    search_fields = ['email', 'otp_code']
