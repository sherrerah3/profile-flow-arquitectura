from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)  # Hacemos el email único
    is_recruiter = models.BooleanField(default=False)  # Campo extra: ¿Es reclutador?
    pass
    
    def __str__(self):
        return self.username
