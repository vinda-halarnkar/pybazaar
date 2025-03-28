from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticates a user based on email and password. Overrides the default authenticate method.

        Parameters:
        request (HttpRequest): The current request object.
        username (str): The email address of the user.
        password (str): The password of the user.
        **kwargs: Additional keyword arguments.

        Returns:
        User: The authenticated user if the credentials are valid, otherwise None.
        """
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
