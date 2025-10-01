from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, RegisterSerializer
from .auth_factory import AuthStrategyFactory

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Endpoint de login que utiliza Factory Pattern para crear estrategias de autenticación.
        
        El cliente puede especificar el tipo de autenticación mediante el campo 'auth_type':
        - 'username' o 'username_password': Autenticación por usuario/contraseña
        - 'email' o 'email_password': Autenticación por email/contraseña
        
        Body del request:
        {
            "auth_type": "username",  // Opcional, por defecto 'username_password'
            "username": "usuario",    // Para auth_type username
            "password": "contraseña"
        }
        
        O para email:
        {
            "auth_type": "email",
            "email": "usuario@email.com",
            "password": "contraseña"
        }
        """
        # Factory Pattern en acción - estrategia dinámica
        auth_type = request.data.get('auth_type', 'username_password')
        
        try:
            # El Factory crea la estrategia apropiada
            auth_strategy = AuthStrategyFactory.create_strategy(auth_type)
            
            # Autenticar usando la estrategia seleccionada
            user = auth_strategy.authenticate(request.data)
            
            # Crear o obtener token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                "token": token.key,
                "user": UserSerializer(user).data,
                "auth_method": auth_type,  # Información adicional para el cliente
                "message": f"Login exitoso usando {auth_type}"
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            # Error del Factory (estrategia no válida)
            return Response({
                "error": str(e),
                "available_strategies": AuthStrategyFactory.get_available_strategies()
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            # Error de autenticación u otros errores
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

# Vista que permite GET, PUT y PATCH para el usuario autenticado
class CurrentUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user