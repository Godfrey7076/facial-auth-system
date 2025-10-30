from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from facial_auth.models import UserProfile, SecurityArea
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Create UserProfile for all existing users and fix authentication'

    def handle(self, *args, **options):
        all_users = User.objects.all()

        for user in all_users:
            # Check if profile already exists
            if not hasattr(user, 'userprofile'):
                # Determine user type based on superuser status
                if user.is_superuser:
                    user_type = 'admin'
                    access_level = 5
                    security_number = f"ADMIN_{user.username}"
                    pass_days = 365*5  # 5 years for admins
                elif user.is_staff:
                    user_type = 'security'
                    access_level = 4
                    security_number = f"SEC_{user.username}"
                    pass_days = 365  # 1 year for staff
                else:
                    user_type = 'staff'
                    access_level = 2
                    security_number = f"USER_{user.id}"
                    pass_days = 30  # 30 days for regular users

                # Create user profile
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
                    self.style.SUCCESS(
                        f'Created profile for: {user.username} ({user_type})')
                )
            else:
                # Update existing profile if needed
                profile = user.userprofile
                if user.is_superuser and profile.user_type != 'admin':
                    profile.user_type = 'admin'
                    profile.access_level = 5
                    profile.save()
                    self.stdout.write(
                        self.style.WARNING(
                            f'Updated profile for admin: {user.username}')
                    )
                self.stdout.write(
                    self.style.WARNING(
                        f'Profile already exists for: {user.username}')
                )

        self.stdout.write(
            self.style.SUCCESS('All user profiles have been fixed!')
        )
