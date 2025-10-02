from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .serializers import JobSerializer
from .repositories.django_repo import DjangoORMJobRepository
from .services.job_service import JobService

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .serializers import JobSerializer
from .repositories.django_repo import DjangoORMJobRepository
from .services.job_service import JobService
from .models import Company, Location, Keyword

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

class CompanyOptionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        companies = Company.objects.all().order_by('name')
        data = [{'id': company.id, 'name': company.name} for company in companies]
        return Response(data)

class LocationOptionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        locations = Location.objects.all().order_by('name')
        data = [{'id': location.id, 'name': location.name} for location in locations]
        return Response(data)

class KeywordOptionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        keywords = Keyword.objects.all().order_by('name')
        data = [{'id': keyword.id, 'name': keyword.name} for keyword in keywords]
        return Response(data)