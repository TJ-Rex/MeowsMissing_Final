from django.db import models
import datetime
from cloudinary.models import CloudinaryField

class Reporte(models.Model):
    Nombres = models.CharField(max_length=300)
    Apellidos = models.CharField(max_length=300)
    Contacto = models.CharField(max_length=300)
    Descripcion = models.TextField(max_length=5000)
    Imagen = CloudinaryField('image')
    Fecha = models.DateField(datetime.date.today)
    Estado = models.CharField(max_length=300)

    
    


