from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from facial_auth.models import UserProfile
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Create UserProfile for existing admin users'

    def handle(self, *args, **options):
        admin_users = User.objects.filter(is_superuser=True)

        for user in admin_users:
            # Check if profile already exists
            if not hasattr(user, 'userprofile'):
                UserProfile.objects.create(
                    user=user,
                    security_number=f"ADMIN_{user.username}",
                    user_type='admin',
                    access_level=5,
                    face_encoding="[]",
                    pass_expires=datetime.now() + timedelta(days=365*5)
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created profile for admin: {user.username}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Profile already exists for: {user.username}')
                )
