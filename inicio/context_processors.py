from .models import Notificacion

def notificaciones_contador(request):
    if request.user.is_authenticated:
        total_notificaciones = Notificacion.objects.filter(user=request.user, visto=False).count()
    else:
        total_notificaciones = 0

    return {
        'total_notificaciones': total_notificaciones,
    }
