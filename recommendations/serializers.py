from rest_framework import serializers
from jobs.models import Job

class JobRecommendationSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source="company.name", read_only=True)
    location = serializers.CharField(source="location.name", read_only=True)
    keywords = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    similarity = serializers.FloatField()

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'company', 'location', 'keywords', 'similarity']
