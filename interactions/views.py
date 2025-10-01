from rest_framework import generics, permissions
from .models import Interaction
from .serializers import InteractionSerializer
from .observers import get_like_subject

class CreateInteractionView(generics.CreateAPIView):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Crea una interacción y notifica a observadores usando Observer Pattern.
        """
        interaction = serializer.save(user=self.request.user)
        
        # Observer Pattern en acción - Solo notificar para likes
        if interaction.interaction_type == 'like':
            # Calcular total de likes para esta vacante
            total_likes = Interaction.objects.filter(
                job=interaction.job, 
                interaction_type='like'
            ).count()
            
            # Preparar datos para los observadores
            like_data = {
                'user_id': interaction.user.id,
                'user_name': interaction.user.username,
                'job_id': interaction.job.id,
                'job_title': interaction.job.title,
                'total_likes': total_likes,
                'interaction_id': interaction.id,
            }
            
            # Notificar a todos los observadores
            like_subject = get_like_subject()
            like_subject.notify_like_created(like_data)

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
    
    def perform_destroy(self, instance):
        """
        Elimina una interacción y notifica a observadores usando Observer Pattern.
        """
        # Observer Pattern - Solo notificar para likes
        if instance.interaction_type == 'like':
            # Calcular total de likes después de eliminar este
            total_likes = Interaction.objects.filter(
                job=instance.job, 
                interaction_type='like'
            ).count() - 1  # -1 porque aún no se ha eliminado
            
            # Preparar datos para los observadores
            like_data = {
                'user_id': instance.user.id,
                'user_name': instance.user.username,
                'job_id': instance.job.id,
                'job_title': instance.job.title,
                'total_likes': total_likes,
                'interaction_id': instance.id,
            }
            
            # Notificar a todos los observadores antes de eliminar
            like_subject = get_like_subject()
            like_subject.notify_like_removed(like_data)
        
        # Proceder con la eliminación
        super().perform_destroy(instance)
