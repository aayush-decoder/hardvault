from django.db import models
from django.conf import settings

class HardwareRecord(models.Model):
    # Client Info
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=15)

    # Owner Info (shop owner)
    owner_name = models.CharField(max_length=100)

    # Unique Code for client (first 3 chars of email + 6 random chars)
    client_code = models.CharField(max_length=20, unique=True, null=True)

    # Link to authenticated user (optional - for backward compatibility)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='hardware_records')

    # System Info
    product_id = models.CharField(max_length=100, blank=True, null=True)
    model_name = models.CharField(max_length=255, blank=True, null=True)

    # RAM Info
    ram_serial = models.CharField(max_length=100, blank=True, null=True)
    ram_manufacturer = models.CharField(max_length=100, blank=True, null=True)
    ram_part_number = models.CharField(max_length=100, blank=True, null=True)

    # Disk Info
    disk_model = models.CharField(max_length=255, blank=True, null=True)
    disk_interface_type = models.CharField(max_length=100, blank=True, null=True)
    disk_serial = models.CharField(max_length=100, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client_name} - {self.client_code}"
