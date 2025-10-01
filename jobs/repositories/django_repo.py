from .base import JobRepository
from jobs.models import Job
from django.shortcuts import get_object_or_404

class DjangoORMJobRepository(JobRepository):
    def create_job(self, title, description, company, location, recruiter, keywords):
        return Job.create_job(title, description, company, location, recruiter, keywords)

    def get_job_by_id(self, job_id):
        return get_object_or_404(Job, id=job_id)

    def list_jobs(self):
        return Job.objects.all()