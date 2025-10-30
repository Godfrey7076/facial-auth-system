from django.contrib import admin

# Import models safely with error handling
try:
    from .models import UserProfile, SecurityArea, AccessLog, VisitorLog, SystemSettings
except ImportError as e:
    print(f"Import error in admin: {e}")
    # Define empty classes if import fails

    class UserProfile:
        pass

    class SecurityArea:
        pass

    class AccessLog:
        pass

    class VisitorLog:
        pass

    class SystemSettings:
        pass

# Use default admin site for now


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type',
                    'security_number', 'access_level', 'is_active']


@admin.register(SecurityArea)
class SecurityAreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'access_level', 'is_active']


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'security_area', 'access_granted', 'access_time']


@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'visit_date', 'entry_time', 'exit_time']


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']
