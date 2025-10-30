from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Reset passwords for all users to "password123" for testing'

    def handle(self, *args, **options):
        users = User.objects.all()

        for user in users:
            user.set_password('password123')
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Reset password for: {user.username}')
            )

        self.stdout.write(
            self.style.SUCCESS(
                'All passwords have been reset to "password123"')
        )
