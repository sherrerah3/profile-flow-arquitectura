from rest_framework import generics, permissions
from .models import Interaction
from .serializers import InteractionSerializer

class CreateInteractionView(generics.CreateAPIView):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

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
