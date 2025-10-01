# interactions/serializers.py

from rest_framework import serializers
from .models import Interaction
from jobs.models import Job


class JobMiniSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source="company.name", read_only=True)
    location = serializers.CharField(source="location.name", read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'title', 'company', 'location']


class InteractionSerializer(serializers.ModelSerializer):
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())
    job_details = JobMiniSerializer(source='job', read_only=True)

    class Meta:
        model = Interaction
        fields = ['id', 'user', 'job', 'job_details', 'interaction_type', 'timestamp']
        read_only_fields = ['user', 'timestamp']

