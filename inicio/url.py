from django.urls import path
from .views import perfil



urlpatterns = [
    path('perfil/', perfil, name='perfil'),  # Ruta para ver y editar el perfil    
]
