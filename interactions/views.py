from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Interaction
from .serializers import InteractionSerializer

class CreateInteractionView(generics.CreateAPIView):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Verificar si la interacción ya existe
        job_id = serializer.validated_data['job'].id
        interaction_type = serializer.validated_data['interaction_type']
        
        existing_interaction = Interaction.objects.filter(
            user=request.user,
            job_id=job_id,
            interaction_type=interaction_type
        ).first()
        
        if existing_interaction:
            # Si ya existe, devolver la interacción existente
            response_serializer = self.get_serializer(existing_interaction)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        
        # Si no existe, crear una nueva
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ListUserInteractionsView(generics.ListAPIView):
    serializer_class = InteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Interaction.objects.filter(user=user)

        job_id = self.request.query_params.get("job")
        interaction_type = self.request.query_params.get("interaction_type")

        if job_id:
            queryset = queryset.filter(job__id=job_id)
        if interaction_type:
            queryset = queryset.filter(interaction_type=interaction_type)

        return queryset

class DeleteInteractionView(generics.DestroyAPIView):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Asegura que solo pueda borrar sus propias interacciones
        return Interaction.objects.filter(user=self.request.user)
