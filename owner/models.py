from django.db import models

class HardwareRecord(models.Model):
    # Client Info
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=15)

    # Owner Info (shop owner)
    owner_name = models.CharField(max_length=100)

    # System Info
    product_id = models.CharField(max_length=100)
    model_name = models.CharField(max_length=255)

    # RAM Info
    ram_serial = models.CharField(max_length=100, blank=True, null=True)
    ram_manufacturer = models.CharField(max_length=100, blank=True, null=True)
    ram_part_number = models.CharField(max_length=100, blank=True, null=True)

    # Disk Info
    disk_model = models.CharField(max_length=255, blank=True, null=True)
    disk_interface_type = models.CharField(max_length=100, blank=True, null=True)
    disk_serial = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.client_name} - {self.model_name}"
