from django.urls import path
from .views import JobListCreateView, JobDetailView, MisVacantesPublicadasView

urlpatterns = [
    path('', JobListCreateView.as_view(), name='job-list-create'),
    path('<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('mias/publicadas/', MisVacantesPublicadasView.as_view(), name='mis-vacantes-publicadas'),
]
