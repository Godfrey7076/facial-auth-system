from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import os
from datetime import datetime, timedelta


def user_face_image_path(instance, filename):
    return f'face_images/user_{instance.user.id}/{filename}'


def pass_photo_path(instance, filename):
    return f'pass_photos/user_{instance.user.id}/{filename}'


class SecurityArea(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    access_level = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1=Lowest, 5=Highest security"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Security Area"
        verbose_name_plural = "Security Areas"
        ordering = ['access_level']

    def __str__(self):
        return f"{self.name} (Level {self.access_level})"


class UserProfile(models.Model):
    USER_TYPES = [
        ('admin', 'System Administrator'),
        ('security', 'Security Officer'),
        ('staff', 'Regular Staff'),
        ('visitor', 'Temporary Visitor'),
        ('contractor', 'Contractor'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='userprofile')
    security_number = models.CharField(max_length=20, unique=True)
    user_type = models.CharField(
        max_length=20, choices=USER_TYPES, default='staff')
    face_encoding = models.TextField(default='[]')
    face_image = models.ImageField(
        upload_to=user_face_image_path, null=True, blank=True)
    pass_photo = models.ImageField(
        upload_to=pass_photo_path, null=True, blank=True)
    access_level = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Maximum security level this user can access"
    )

    # Pass validity
    pass_issued = models.DateTimeField(auto_now_add=True)
    pass_expires = models.DateTimeField(
        default=timezone.now() + timedelta(days=30))
    is_active = models.BooleanField(default=True)

    # Additional info
    department = models.CharField(max_length=100, blank=True, default='')
    position = models.CharField(max_length=100, blank=True, default='')
    phone_number = models.CharField(max_length=20, blank=True, default='')
    emergency_contact = models.TextField(blank=True, default='')

    # Security areas this user can access
    allowed_areas = models.ManyToManyField(SecurityArea, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        full_name = self.user.get_full_name()
        if full_name:
            return f"{full_name} - {self.get_user_type_display()}"
        return f"{self.user.username} - {self.get_user_type_display()}"

    def is_pass_valid(self):
        return self.is_active and timezone.now() < self.pass_expires

    def days_until_expiry(self):
        delta = self.pass_expires - timezone.now()
        return max(0, delta.days)

# Signal to automatically create UserProfile when User is created


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Determine user type based on superuser status
        if instance.is_superuser:
            user_type = 'admin'
            access_level = 5
            security_number = f"ADMIN_{instance.username}"
            pass_days = 365*5
        elif instance.is_staff:
            user_type = 'security'
            access_level = 4
            security_number = f"SEC_{instance.username}"
            pass_days = 365
        else:
            user_type = 'staff'
            access_level = 2
            security_number = f"USER_{instance.id}"
            pass_days = 30

        UserProfile.objects.create(
            user=instance,
            security_number=security_number,
            user_type=user_type,
            access_level=access_level,
            pass_expires=timezone.now() + timedelta(days=pass_days)
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()


class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    security_area = models.ForeignKey(SecurityArea, on_delete=models.CASCADE)
    access_granted = models.BooleanField(default=False)
    access_time = models.DateTimeField(auto_now_add=True)
    access_point = models.CharField(max_length=100, blank=True)
    reason_denied = models.TextField(blank=True)

    # Authentication method used
    authentication_method = models.CharField(max_length=20, choices=[
        ('face', 'Facial Recognition'),
        ('security_number', 'Security Number'),
        ('both', 'Both Methods')
    ])

    class Meta:
        verbose_name = "Access Log"
        verbose_name_plural = "Access Logs"
        ordering = ['-access_time']

    def __str__(self):
        status = "Granted" if self.access_granted else "Denied"
        return f"{self.user.username} - {self.security_area.name} - {status}"


class VisitorLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visit_date = models.DateField(auto_now_add=True)
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)
    purpose = models.TextField()
    hosting_staff = models.CharField(max_length=100, blank=True)
    areas_visited = models.ManyToManyField(SecurityArea, blank=True)

    class Meta:
        verbose_name = "Visitor Log"
        verbose_name_plural = "Visitor Logs"
        ordering = ['-entry_time']

    def __str__(self):
        return f"{self.user.username} - {self.visit_date}"


class SystemSettings(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "System Setting"
        verbose_name_plural = "System Settings"

    def __str__(self):
        return self.key
