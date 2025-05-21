from django.db import models
from django.conf import settings

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    keywords = models.TextField(help_text="Palabras clave separadas por comas, por ejemplo: Python, Django, Remote")

    def __str__(self):
        return self.title
