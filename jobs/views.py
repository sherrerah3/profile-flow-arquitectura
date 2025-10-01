from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .serializers import JobSerializer
from .repositories.django_repo import DjangoORMJobRepository
from .services.job_service import JobService


class JobListCreateView(ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        service = JobService(DjangoORMJobRepository())
        return service.list_jobs()

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_create(self, serializer):
        if not self.request.user.is_recruiter:
            raise PermissionDenied("Solo los reclutadores pueden publicar vacantes.")

        service = JobService(DjangoORMJobRepository())
        job = service.create_job(
            title=serializer.validated_data["title"],
            description=serializer.validated_data["description"],
            company=self.request.data.get("company"),
            location=self.request.data.get("location"),
            recruiter=self.request.user,
            keywords=self.request.data.get("keywords", [])
        )
        serializer.instance = job  # importante para que se devuelva correctamente


class JobDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        service = JobService(DjangoORMJobRepository())
        return service.list_jobs()

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_update(self, serializer):
        job = self.get_object()
        if job.recruiter != self.request.user:
            raise PermissionDenied("No tienes permiso para editar esta vacante.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.recruiter != self.request.user:
            raise PermissionDenied("No tienes permiso para eliminar esta vacante.")
        service = JobService(DjangoORMJobRepository())
        service.delete_job(instance.id)


class MisVacantesPublicadasView(ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_recruiter:
            service = JobService(DjangoORMJobRepository())
            return service.list_jobs_by_recruiter(user)
        return []

    def get_serializer_context(self):
        return {"request": self.request}
