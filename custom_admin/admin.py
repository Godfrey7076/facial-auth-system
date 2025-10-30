from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.urls import path
from django.shortcuts import redirect
from django.views.generic import RedirectView


class CustomAdminSite(admin.AdminSite):
    site_header = 'Security Pass Management System'
    site_title = 'Administration Panel'
    index_title = 'System Administration'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        # Add custom URLs if needed
        custom_urls = [
            # You can add custom URLs here if needed
        ]
        return custom_urls + urls

    def each_context(self, request):
        context = super().each_context(request)
        # Add custom context variables
        context['site_title'] = self.site_title
        context['site_header'] = self.site_header
        return context


# Create global instance
custom_admin_site = CustomAdminSite(name='custom_admin')

# Register models
custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Group, GroupAdmin)
