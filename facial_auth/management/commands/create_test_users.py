from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from facial_auth.models import UserProfile
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Create test users for different roles'

    def handle(self, *args, **options):
        test_users = [
            {'username': 'security1', 'user_type': 'security', 'access_level': 4},
            {'username': 'staff1', 'user_type': 'staff', 'access_level': 2},
            {'username': 'visitor1', 'user_type': 'visitor', 'access_level': 1},
            {'username': 'contractor1', 'user_type': 'contractor', 'access_level': 2},
        ]

        for user_data in test_users:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    password='password123',
                    email=f"{user_data['username']}@test.com",
                    first_name=user_data['username'].title()
                )

                UserProfile.objects.create(
                    user=user,
                    security_number=f"TEST_{user_data['username']}",
                    user_type=user_data['user_type'],
                    access_level=user_data['access_level'],
                    face_encoding="[]",
                    pass_expires=datetime.now() + timedelta(days=30),
                    is_active=True
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created test user: {user_data["username"]}')
                )

        self.stdout.write(
            self.style.SUCCESS('Test users created successfully!')
        )
