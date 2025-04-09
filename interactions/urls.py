from django.urls import path
from .views import CreateInteractionView, ListUserInteractionsView, DeleteInteractionView

urlpatterns = [
    path('', CreateInteractionView.as_view(), name='create_interaction'),
    path('mis/', ListUserInteractionsView.as_view(), name='mis_interacciones'),
    path('<int:pk>/', DeleteInteractionView.as_view(), name='eliminar_interaccion'),
]
