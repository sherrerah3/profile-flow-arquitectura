from django.db import models
from django.contrib.auth import get_user_model
from jobs.models import Job

User = get_user_model()


class Interaction(models.Model):
    INTERACTION_TYPES = [
        ('like', 'Like'),
        ('view', 'View'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="interactions"
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="interactions"
    )
    interaction_type = models.CharField(
        max_length=10,
        choices=INTERACTION_TYPES
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job', 'interaction_type')
        ordering = ['-timestamp']
        verbose_name = "Interaction"
        verbose_name_plural = "Interactions"

    def __str__(self):
        return f"{self.user.username} - {self.interaction_type} - {self.job.title} @ {self.job.company.name} ({self.job.location.name})"
