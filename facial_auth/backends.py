from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Authenticate against either username or email
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('username')

        try:
            # Try to fetch user by username or email
            user = User.objects.get(
                Q(username__iexact=username) |
                Q(email__iexact=username)
            )
        except User.DoesNotExist:
            # Run the default password hasher once to reduce timing difference
            User().set_password(password)
            return None
        except User.MultipleObjectsReturned:
            # Multiple users found - should not happen with proper constraints
            user = User.objects.filter(
                Q(username__iexact=username) |
                Q(email__iexact=username)
            ).first()

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
