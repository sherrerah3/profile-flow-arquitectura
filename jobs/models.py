from django.db import models
from django.conf import settings


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Keyword(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="jobs")
    created_at = models.DateTimeField(auto_now_add=True)
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    keywords = models.ManyToManyField(Keyword, related_name="jobs")

    def __str__(self):
        return self.title

    @classmethod
    def create_job(cls, title, description, company_name, location_name, recruiter, keywords_list):
        """
        Crea un job normalizado a partir de strings de company, location y lista de keywords.
        """
        company, _ = Company.objects.get_or_create(name=company_name)
        location, _ = Location.objects.get_or_create(name=location_name)

        job = cls.objects.create(
            title=title,
            description=description,
            company=company,
            location=location,
            recruiter=recruiter,
        )

        # Normaliza las palabras clave
        for kw in keywords_list:
            kw_clean = kw.strip().lower()
            if kw_clean:
                keyword_obj, _ = Keyword.objects.get_or_create(name=kw_clean)
                job.keywords.add(keyword_obj)

        return job
