# serializers.py
from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['recruiter', 'created_at']

    def create(self, validated_data):
        recruiter = validated_data.pop('recruiter')
        return Job.create_job(recruiter=recruiter, **validated_data)