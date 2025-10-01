from rest_framework import serializers
from .models import Job, Keyword


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ["id", "name"]


class JobSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source="company.name", read_only=True)
    location = serializers.CharField(source="location.name", read_only=True)
    # Opción 1 → mostrar lista de objetos con id y name:
    # keywords = KeywordSerializer(many=True, read_only=True)

    # Opción 2 → mostrar solo la lista de nombres (más limpio):
    keywords = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "company",
            "location",
            "keywords",
            "created_at",
            "is_owner"
        ]
        read_only_fields = ["recruiter", "created_at"]

    def get_is_owner(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return obj.recruiter == request.user
        return False
