from django.db import models
import datetime

class Post(models.Model):
    Titulo = models.CharField(max_length=300)
    Descripcion = models.TextField(max_length=5000)
    Imagen = models.ImageField(upload_to='noticias/images')
    Fecha = models.DateField(default=datetime.date.today)  # Corrige para usar `default`
    Autor = models.CharField(max_length=200)  # Nuevo campo para el autor

    def __str__(self):
        return self.Titulo

from django.contrib.auth.models import User

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comentarios")
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(max_length=1000)
    fecha = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Comentario de {self.autor} en {self.post.Titulo}"