from rest_framework.views import APIView 
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from .models import Job
from .serializers import JobSerializer

class JobListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        jobs = Job.objects.all().order_by('-created_at')
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_recruiter:
            return Response(
                {"error": "Solo los reclutadores pueden publicar vacantes."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(recruiter=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk)

        # ✅ Permitir a usuarios normales ver cualquier vacante
        # ✅ Permitir a reclutadores ver solo las suyas
        if request.user.is_recruiter and job.recruiter != request.user:
            raise PermissionDenied("Los reclutadores no pueden ver detalles de vacantes ajenas.")

        serializer = JobSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk):
        job = get_object_or_404(Job, pk=pk)

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
        job = get_object_or_404(Job, pk=pk)

        if job.recruiter != request.user:
            return Response(
                {"error": "No tienes permiso para eliminar esta vacante."},
                status=status.HTTP_403_FORBIDDEN
            )

        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MisVacantesPublicadasView(ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_recruiter:
            return Job.objects.filter(recruiter=user).order_by('-created_at')
        return Job.objects.none()
