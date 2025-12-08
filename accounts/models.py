from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string
from datetime import timedelta
from django.utils import timezone


class User(AbstractUser):
    """Base user model"""
    USER_TYPE_CHOICES = (
        ('owner', 'Owner'),
        ('client', 'Client'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.user_type})"


class Owner(models.Model):
    """Owner profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile')
    company_name = models.CharField(max_length=255)
    invitation_code = models.CharField(max_length=20, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.invitation_code:
            self.invitation_code = self.generate_invitation_code()
        super().save(*args, **kwargs)
    
    def generate_invitation_code(self):
        """Generate unique invitation code"""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            if not Owner.objects.filter(invitation_code=code).exists():
                return code
    
    def __str__(self):
        return f"{self.company_name} - {self.user.email}"


class Client(models.Model):
    """Client profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    owners = models.ManyToManyField(Owner, related_name='clients', blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.user.email}"


class OTP(models.Model):
    """OTP model for verification"""
    OTP_TYPE_CHOICES = (
        ('registration', 'Registration'),
        ('password_reset', 'Password Reset'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps', null=True, blank=True)
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    otp_type = models.CharField(max_length=20, choices=OTP_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.otp_code:
            self.otp_code = self.generate_otp()
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)
    
    def generate_otp(self):
        """Generate 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=6))
    
    def is_valid(self):
        """Check if OTP is still valid"""
        return not self.is_verified and timezone.now() < self.expires_at
    
    def __str__(self):
        return f"{self.email} - {self.otp_code} ({self.otp_type})"
