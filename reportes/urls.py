from django.urls import path
from .views import render_reportes, reportes_detail, crear_reporte
from .views import render_reportes, reportes_detail, crear_reporte, eliminar_reporte



app_name = 'reportes'

urlpatterns = [
    path('', render_reportes, name='reportes'),  # Ruta para listar reportes
    path('<int:reporte_id>/', reportes_detail, name='reportes_details'),  # Ruta para detalles de un reporte
    path('crear/', crear_reporte, name='crear_reporte'),  # Ruta para crear un reporte
    path('eliminar/<int:reporte_id>/', eliminar_reporte, name='eliminar_reporte'),  # Ruta para eliminar reporte

]

