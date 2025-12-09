from django.contrib import admin
from .models import User, Owner, OTP

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'user_type', 'is_approved', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_approved', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    actions = ['approve_owners']
    
    def approve_owners(self, request, queryset):
        """Approve selected owner accounts"""
        updated = queryset.filter(user_type='owner', is_approved=False).update(
            is_approved=True,
            is_active=True
        )
        self.message_user(request, f'{updated} owner(s) approved successfully.')
    approve_owners.short_description = 'Approve selected owners'

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'invitation_code', 'is_approved']
    list_filter = ['user__is_approved']
    search_fields = ['company_name', 'user__email']
    
    def is_approved(self, obj):
        return obj.user.is_approved
    is_approved.boolean = True
    is_approved.short_description = 'Approved'

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['email', 'otp_code', 'otp_type', 'created_at', 'expires_at', 'is_verified']
    list_filter = ['otp_type', 'is_verified']
    search_fields = ['email', 'otp_code']
