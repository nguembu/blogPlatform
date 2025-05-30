from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class EmailAuthBackend(ModelBackend):
    """
    Authentification par email ou username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Permettre l'authentification par email ou username
        if username is None:
            username = kwargs.get('email')
        if username is None or password is None:
            return None
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
