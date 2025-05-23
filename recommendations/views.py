from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services.tfidf_recommender import recomendar_vacantes
from jobs.serializers import JobSerializer

class JobRecommendationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        recomendaciones = recomendar_vacantes(user)
        serializer = JobSerializer(recomendaciones, many=True)
        return Response(serializer.data)
