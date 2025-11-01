from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, SecurityArea, AccessLog, VisitorLog, SystemSettings


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_info', 'user_type', 'security_number',
                    'access_level', 'pass_status', 'is_active']
    list_filter = ['user_type', 'access_level', 'is_active', 'pass_issued']
    search_fields = ['user__username', 'user__first_name',
                     'user__last_name', 'security_number']
    readonly_fields = ['created_at', 'updated_at', 'pass_issued']
    filter_horizontal = ['allowed_areas']

    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'security_number', 'user_type')
        }),
        ('Security Settings', {
            'fields': ('access_level', 'allowed_areas')
        }),
        ('Pass Information', {
            'fields': ('pass_issued', 'pass_expires', 'is_active')
        }),
        ('Additional Information', {
            'fields': ('department', 'position', 'phone_number', 'emergency_contact'),
            'classes': ('collapse',)
        }),
        ('Biometric Data', {
            'fields': ('face_encoding', 'face_image', 'pass_photo'),
            'classes': ('collapse',)
        }),
    )

    def user_info(self, obj):
        full_name = obj.user.get_full_name()
        if full_name:
            return f"{full_name} ({obj.user.username})"
        return obj.user.username
    user_info.short_description = 'User'

    def pass_status(self, obj):
        if obj.is_pass_valid():
            return format_html('<span style="color: green;">✓ Valid</span>')
        else:
            return format_html('<span style="color: red;">✗ Expired</span>')
    pass_status.short_description = 'Pass Status'


@admin.register(SecurityArea)
class SecurityAreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'access_level', 'is_active', 'created_at']
    list_filter = ['is_active', 'access_level']
    search_fields = ['name', 'description']

    fieldsets = (
        ('Area Information', {
            'fields': ('name', 'description', 'access_level')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'security_area', 'access_granted',
                    'access_time', 'authentication_method']
    list_filter = ['access_granted', 'security_area',
                   'authentication_method', 'access_time']
    search_fields = ['user__username', 'security_area__name']
    readonly_fields = ['access_time']

    def has_add_permission(self, request):
        return False


@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'visit_date',
                    'entry_time', 'exit_time', 'purpose_short']
    list_filter = ['visit_date', 'hosting_staff']
    search_fields = ['user__username', 'purpose', 'hosting_staff']

    def purpose_short(self, obj):
        return obj.purpose[:50] + '...' if len(obj.purpose) > 50 else obj.purpose
    purpose_short.short_description = 'Purpose'


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ['key', 'value_short', 'description']
    search_fields = ['key', 'description']

    def value_short(self, obj):
        return obj.value[:100] + '...' if len(obj.value) > 100 else obj.value
    value_short.short_description = 'Value'
