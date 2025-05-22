from django.db import models
from django.conf import settings

class Question(models.Model):
    text = models.TextField()
    options = models.JSONField()  # Lista de opciones, ejemplo: ["Opción 1", "Opción 2", ...]
    created_at = models.DateTimeField(auto_now_add=True)

class UserQuestionAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=255)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')  # evita respuestas duplicadas
