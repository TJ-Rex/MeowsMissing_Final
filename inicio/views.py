from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from .models import Link
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q


from datetime import timedelta
from noticias.models import Post
from reportes.models import Reporte
from .models import Notificacion
from .models import Link
from django.contrib.auth.hashers import make_password





def home(request):
    return render(request, 'home.html')

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
        'form': UserCreationForm,
       })
    else:
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        

        if request.POST ['password1'] == request.POST ['password2']:
           try:
               user = User.objects.create_user(username=request.POST['username'], 
               password= request.POST['password1'])
               user.email = email
               user.first_name = first_name
               user.last_name = last_name
               user.save()
               login(request, user)
               return redirect('inicio')           
           except:
               return render(request, 'signup.html', {
               'form': UserCreationForm,
               'error': 'Username already exist'
               })
        return render(request, 'signup.html', {
               'form': UserCreationForm,
               'error':'Password do not match'
               })


def inicio(request):
    links = Link.objects.all()

    return render(request, 'inicio.html', {'links': links})

def signout(request):
    logout(request)
    return redirect ('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            "form": AuthenticationForm
            })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, 'signin.html', {
                "form": AuthenticationForm, 
                "error": "Username or password is incorrect."})
        else:
            login(request, user)
            return redirect('inicio')
        
def perfil(request):
    """Muestra y permite editar el perfil del usuario, cambiar contraseña o eliminar cuenta."""
    if request.method == 'POST':
        if 'update_profile' in request.POST:  # Actualizar perfil
            try:
                user = request.user
                user.username = request.POST.get('username', user.username)
                user.email = request.POST.get('email', user.email)
                user.first_name = request.POST.get('first_name', user.first_name)
                user.last_name = request.POST.get('last_name', user.last_name)
                user.save()
                messages.success(request, 'Perfil actualizado exitosamente.')
            except Exception as e:
                messages.error(request, f'Error al actualizar perfil: {e}')

        elif 'change_password' in request.POST:  # Cambiar contraseña
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, request.user)  # Mantener sesión activa
                messages.success(request, 'Contraseña actualizada exitosamente.')
            else:
                messages.error(request, 'Por favor corrige los errores en el formulario de contraseña.')

        elif 'delete_account' in request.POST:  # Eliminar cuenta
            user = request.user
            logout(request)
            user.delete()
            messages.success(request, 'Cuenta eliminada exitosamente.')
            return redirect('home')

        return redirect('perfil')

    password_form = PasswordChangeForm(user=request.user)
    return render(request, 'perfil.html', {'user': request.user, 'password_form': password_form})


@login_required
def notificaciones(request):
    # Obtener todas las notificaciones del usuario
    notificaciones_usuario = Notificacion.objects.filter(user=request.user).order_by('-fecha_creacion')

    # Separar noticias y reportes
    noticias = []
    reportes = []

    for notif in notificaciones_usuario:
        if notif.tipo == 'noticia':
            try:
                noticias.append(Post.objects.get(id=notif.objeto_id))
            except Post.DoesNotExist:
                pass  # Si la noticia fue eliminada, no hacer nada
        elif notif.tipo == 'reporte':
            try:
                reportes.append(Reporte.objects.get(id=notif.objeto_id))
            except Reporte.DoesNotExist:
                pass  # Si el reporte fue eliminado, no hacer nada

    # Marcar como vistas las notificaciones no vistas
    notificaciones_usuario.filter(visto=False).update(visto=True)

    return render(request, 'notificaciones.html', {
        'noticias': noticias,
        'reportes': reportes,
        'total_notificaciones': 0,  # Reinicia el contador
    })
    
    


@login_required
def links_admin(request):
    if not request.user.is_staff:  # Asegúrate de que solo el administrador pueda acceder
        return redirect('home')

    if request.method == 'POST':
        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']
        imagen = request.FILES.get('imagen')
        url = request.POST.get('url', '')
        
          # Agregar un mensaje de éxito
        messages.success(request, '¡Link creado exitosamente!')

        Link.objects.create(Titulo=titulo, Descripcion=descripcion, Imagen=imagen, Url=url)
        return redirect('links_admin')

    links = Link.objects.all()
    return render(request, 'links_admin.html', {'links': links})



@login_required
@user_passes_test(lambda u: u.is_staff)  # Solo para usuarios con rol de staff/admin
def gestionar_usuarios(request):
    query = request.GET.get('q', '')  # Parámetro de búsqueda
    usuarios = User.objects.all()

    if query:
        usuarios = usuarios.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        accion = request.POST.get('accion')

        user = User.objects.get(pk=user_id)

        if accion == 'hacer_admin':
            user.is_staff = True
            user.save()
            messages.success(request, f'{user.username} ahora es administrador.')
        elif accion == 'eliminar_usuario':
            user.delete()
            messages.success(request, f'{user.username} ha sido eliminado.')

        return redirect('gestionar_usuarios')

    return render(request, 'gestionar_usuarios.html', {'usuarios': usuarios})









def cambiar_contrasena(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Validar que las contraseñas coincidan
        if new_password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('cambiar_contrasena')

        try:
            # Verificar si existe un usuario con el username y email proporcionados
            user = User.objects.get(username=username, email=email)
            # Cambiar la contraseña
            user.password = make_password(new_password)
            user.save()
            messages.success(request, 'Contraseña actualizada exitosamente.')
            return redirect('signin')
        except User.DoesNotExist:
            messages.error(request, 'Usuario o correo electrónico incorrectos.')
            return redirect('cambiar_contrasena')

    return render(request, 'cambiar_contrasena.html')

