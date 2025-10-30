from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from facial_auth.models import UserProfile
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Completely fix authentication system and user profiles'

    def handle(self, *args, **options):
        self.stdout.write("Fixing authentication system...")

        # 1. Ensure all users have profiles
        users_without_profiles = User.objects.filter(userprofile__isnull=True)
        for user in users_without_profiles:
            if user.is_superuser:
                user_type = 'admin'
                access_level = 5
                security_number = f"ADMIN_{user.username}"
                pass_days = 365*5
            elif user.is_staff:
                user_type = 'security'
                access_level = 4
                security_number = f"SEC_{user.username}"
                pass_days = 365
            else:
                user_type = 'staff'
                access_level = 2
                security_number = f"USER_{user.id}"
                pass_days = 30

            UserProfile.objects.create(
                user=user,
                security_number=security_number,
                user_type=user_type,
                access_level=access_level,
                face_encoding="[]",
                pass_expires=datetime.now() + timedelta(days=pass_days),
                is_active=True
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created profile for: {user.username}')
            )

        # 2. Reset all passwords to 'password123' for testing
        for user in User.objects.all():
            user.set_password('password123')
            user.save()

        self.stdout.write(
            self.style.SUCCESS('Reset all passwords to "password123"')
        )

        # 3. Ensure superusers are admins
        superusers = User.objects.filter(is_superuser=True)
        for user in superusers:
            if hasattr(user, 'userprofile'):
                profile = user.userprofile
                if profile.user_type != 'admin':
                    profile.user_type = 'admin'
                    profile.access_level = 5
                    profile.save()
                    self.stdout.write(
                        self.style.WARNING(f'Updated {user.username} to admin')
                    )

        self.stdout.write(
            self.style.SUCCESS('Authentication system fixed successfully!')
        )
        self.stdout.write(
            self.style.SUCCESS(
                'You can now login with any username and password "password123"')
        )
