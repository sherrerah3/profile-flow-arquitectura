from django.contrib import admin
from .models import Job, Company, Location, Keyword


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "recruiter", "created_at")
    search_fields = ("title", "description")
    list_filter = ("company", "location", "recruiter", "created_at")
    filter_horizontal = ("keywords",) 


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)