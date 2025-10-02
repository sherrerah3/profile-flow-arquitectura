from django.urls import path
from .views import (
    JobListCreateView, 
    JobDetailView, 
    MisVacantesPublicadasView,
    CompanyOptionsView,
    LocationOptionsView, 
    KeywordOptionsView
)

urlpatterns = [
    path('', JobListCreateView.as_view(), name='job-list-create'),
    path('<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('mias/publicadas/', MisVacantesPublicadasView.as_view(), name='mis-vacantes-publicadas'),
    path('companies/', CompanyOptionsView.as_view(), name='company-options'),
    path('locations/', LocationOptionsView.as_view(), name='location-options'),
    path('keywords/', KeywordOptionsView.as_view(), name='keyword-options'),
]