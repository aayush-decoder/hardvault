from django.contrib import admin
from .models import HardwareRecord

@admin.register(HardwareRecord)
class HardwareRecordAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email', 'owner_name', 'model_name', 'product_id')
    search_fields = ('client_name', 'client_email', 'owner_name', 'model_name', 'product_id')
