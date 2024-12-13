from django.db import models
from django.contrib.auth.models import User
from django.apps import apps  # Para evitar ciclos de importación



class Link(models.Model):
    Titulo = models.CharField(max_length=100)
    Descripcion = models.CharField(max_length=250)
    Imagen = models.ImageField(upload_to="inicio/images/")
    Url = models.URLField(blank=True)

    def __str__(self):
        return self.Titulo
    

class Notificacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)  # 'noticia' o 'reporte'
    objeto_id = models.PositiveIntegerField()  # ID del objeto relacionado (Post o Reporte)
    visto = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def get_objeto(self):
        """Devuelve el objeto relacionado (Post o Reporte)."""
        if self.tipo == 'noticia':
            return apps.get_model('noticias', 'Post').objects.get(id=self.objeto_id)
        elif self.tipo == 'reporte':
            return apps.get_model('reportes', 'Reporte').objects.get(id=self.objeto_id)
        return None

    def __str__(self):
        return f"{self.user.username} - {self.tipo} - {'Visto' if self.visto else 'No visto'}"

