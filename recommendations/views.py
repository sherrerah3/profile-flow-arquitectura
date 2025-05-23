from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services.tfidf_recommender import recomendar_vacantes

class JobRecommendationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recomendaciones = recomendar_vacantes(request.user)
        data = [
            {
                "id": job.id,
                "title": job.title,
                "description": job.description,
                "similarity": job.similarity,
                "company": job.company,
                "location": job.location,
            }
            for job in recomendaciones
        ]
        return Response(data)
