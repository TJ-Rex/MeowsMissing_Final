from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Reporte
from django.utils import timezone
from django.db.models import Q

from inicio.models import Notificacion
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required



def crear_reporte(request):
    """Vista para manejar la creación de un nuevo reporte."""
    if request.method == 'POST':
        nombres = request.POST.get('Nombres')
        apellidos = request.POST.get('Apellidos')
        contacto = request.POST.get('Contacto')
        descripcion = request.POST.get('Descripcion')
        imagen = request.FILES.get('Imagen')
        fecha = request.POST.get('Fecha')
        estado = request.POST.get('Estado')

        nuevo_reporte = Reporte(
            Nombres=nombres,
            Apellidos=apellidos,
            Contacto=contacto,
            Descripcion=descripcion,
            Imagen=imagen,
            Fecha=fecha if fecha else timezone.now().date(),
            Estado=estado
        )
        nuevo_reporte.save()

        for user in User.objects.all():
            Notificacion.objects.create(user=user, tipo='reporte', objeto_id=nuevo_reporte.id)

        messages.success(request, '¡Reporte creado exitosamente!')
        return redirect('reportes:crear_reporte')

    return render(request, 'crear_reporte.html')

def render_reportes(request):
    """Vista para mostrar la lista de reportes con filtro de búsqueda."""
    query = request.GET.get('q', '')  # Buscar texto ingresado
    estado = request.GET.get('estado', '')  # Filtrar por estado
    fecha = request.GET.get('fecha', '')  # Filtrar por fecha

    # Obtiene todos los reportes
    reportes = Reporte.objects.all()

    # Aplica filtros si hay parámetros en la solicitud
    if query:
        reportes = reportes.filter(
            Q(Nombres__icontains=query) | Q(Apellidos__icontains=query) | Q(Descripcion__icontains=query)
        )
    if estado:
        reportes = reportes.filter(Estado=estado)
    if fecha:
        reportes = reportes.filter(Fecha=fecha)

    return render(request, 'reportes.html', {'reportes': reportes})

def reportes_detail(request, reporte_id):
    """Vista para mostrar los detalles de un reporte."""
    reporte = get_object_or_404(Reporte, pk=reporte_id)
    return render(request, 'reportes_details.html', {'reporte': reporte})

@staff_member_required
def eliminar_reporte(request, reporte_id):
    """Vista para eliminar un reporte por su ID."""
    reporte = get_object_or_404(Reporte, pk=reporte_id)
    reporte.delete()
    messages.success(request, '¡Reporte eliminado exitosamente!')
    return redirect('reportes:reportes')