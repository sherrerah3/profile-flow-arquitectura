from django.urls import path
from .views import JobRecommendationsView

urlpatterns = [
    path('', JobRecommendationsView.as_view(), name='job-recommendations'),
]
