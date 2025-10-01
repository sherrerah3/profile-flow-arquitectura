from rest_framework.views import APIView 
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from .serializers import JobSerializer
from .repositories.django_repo import DjangoORMJobRepository
from .services.job_service import JobService

class JobListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = JobService(DjangoORMJobRepository())
        jobs = service.list_jobs()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_recruiter:
            return Response(
                {"error": "Solo los reclutadores pueden publicar vacantes."},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data
        service = JobService(DjangoORMJobRepository())
        job = service.create_job(
            title=data.get("title"),
            description=data.get("description"),
            company=data.get("company"),
            location=data.get("location"),
            recruiter=request.user,
            keywords=data.get("keywords", "general")
        )
        serializer = JobSerializer(job)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        service = JobService(DjangoORMJobRepository())
        job = service.get_job(pk)

        if request.user.is_recruiter and job.recruiter != request.user:
            raise PermissionDenied("Los reclutadores no pueden ver detalles de vacantes ajenas.")

        serializer = JobSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk):
        service = JobService(DjangoORMJobRepository())
        job = service.get_job(pk)

        if job.recruiter != request.user:
            return Response(
                {"error": "No tienes permiso para editar esta vacante."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        service = JobService(DjangoORMJobRepository())
        job = service.get_job(pk)

        if job.recruiter != request.user:
            return Response(
                {"error": "No tienes permiso para eliminar esta vacante."},
                status=status.HTTP_403_FORBIDDEN
            )

        service.delete_job(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MisVacantesPublicadasView(ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_recruiter:
            service = JobService(DjangoORMJobRepository())
            return service.list_jobs_by_recruiter(user)
        return []
