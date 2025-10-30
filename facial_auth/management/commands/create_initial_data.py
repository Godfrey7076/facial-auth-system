from django.core.management.base import BaseCommand
from facial_auth.models import SecurityArea, SystemSettings
from datetime import datetime


class Command(BaseCommand):
    help = 'Create initial security areas and system settings'

    def handle(self, *args, **options):
        # Create security areas
        areas = [
            {'name': 'Main Entrance',
                'description': 'Primary building entrance', 'access_level': 1},
            {'name': 'Office Area',
                'description': 'General office workspace', 'access_level': 2},
            {'name': 'Server Room',
                'description': 'IT infrastructure room', 'access_level': 4},
            {'name': 'Executive Floor',
                'description': 'Management offices', 'access_level': 3},
            {'name': 'Research Lab',
                'description': 'Restricted research area', 'access_level': 5},
        ]

        for area_data in areas:
            area, created = SecurityArea.objects.get_or_create(
                name=area_data['name'],
                defaults=area_data
            )
            if created:
                self.stdout.write(f"Created security area: {area.name}")

        # Create system settings
        settings = [
            {'key': 'system_name', 'value': 'High Security Pass Management System',
                'description': 'System display name'},
            {'key': 'max_pass_duration', 'value': '365',
                'description': 'Maximum pass duration in days'},
            {'key': 'face_similarity_threshold', 'value': '0.8',
                'description': 'Minimum face similarity score for authentication'},
            {'key': 'auto_logout_minutes', 'value': '30',
                'description': 'Auto logout after minutes of inactivity'},
        ]

        for setting_data in settings:
            setting, created = SystemSettings.objects.get_or_create(
                key=setting_data['key'],
                defaults=setting_data
            )
            if created:
                self.stdout.write(f"Created system setting: {setting.key}")

        self.stdout.write(
            self.style.SUCCESS('Initial data created successfully!')
        )
