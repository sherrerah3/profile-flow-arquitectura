from rest_framework import serializers
from jobs.models import Job

class JobRecommendationSerializer(serializers.ModelSerializer):
    similarity = serializers.FloatField()

    class Meta:
        model = Job
<<<<<<< HEAD
        fields = ['id', 'title', 'description', 'keywords', 'similarity']
=======
        fields = ['id', 'title', 'description', 'keywords', 'similarity']
>>>>>>> Samuel
