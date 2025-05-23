from django.contrib.auth import authenticate, get_user_model
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

class AuthenticationStrategy:
    def authenticate(self, data):
        raise NotImplementedError("Debes implementar el método authenticate()")

class UsernamePasswordAuthStrategy(AuthenticationStrategy):
    def authenticate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed("Credenciales incorrectas")
        return user

class EmailPasswordAuthStrategy(AuthenticationStrategy):
    def authenticate(self, data):
        email = data.get("email")
        password = data.get("password")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed("Usuario con este correo no existe")

        if not user.check_password(password):
            raise AuthenticationFailed("Contraseña incorrecta")

        return user
