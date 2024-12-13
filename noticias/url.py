from django.urls import path
from .views import render_posts, post_detail, crear_post
from . import views


app_name = 'noticias'

urlpatterns = [
    path('', render_posts, name='posts'),  # Ruta para listar posts
    path('<int:post_id>/', post_detail, name='post_detail'),  # Ruta para los detalles de un post
    path('crear/', crear_post, name='crear_post'),  # Ruta para crear un nuevo post
    path('eliminar/<int:post_id>/', views.eliminar_post, name='eliminar_post'),
    path('eliminar_comentario/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
]

