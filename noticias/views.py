from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Post
from django.utils import timezone

from django.contrib.auth.decorators import user_passes_test

from inicio.models import Notificacion
from django.contrib.auth.models import User
from .models import Comentario
from .forms import ComentarioForm

from django.contrib.auth.decorators import login_required


def render_posts(request):
    """Vista para listar todas las noticias."""
    posts = Post.objects.all().order_by('-Fecha')  # Ordenadas por fecha descendente
    return render(request, 'posts.html', {'posts': posts})

from .models import Comentario
from .forms import ComentarioForm

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comentarios = post.comentarios.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.post = post
                comentario.autor = request.user
                comentario.save()
                return redirect('noticias:post_detail', post_id=post.id)
        else:
            messages.error(request, "Debes iniciar sesión para comentar.")
            return redirect('login')  # Ajusta la URL de tu login

    else:
        form = ComentarioForm()

    return render(request, 'post_details.html', {
        "post": post,
        "comentarios": comentarios,
        "form": form,
    })

def crear_post(request):
    """Vista para manejar la creación de un nuevo post."""
    if request.method == 'POST':
        # Obtener los datos del formulario
        titulo = request.POST.get('Titulo')
        descripcion = request.POST.get('Descripcion')
        imagen = request.FILES.get('Imagen')
        fecha = request.POST.get('Fecha')
        autor = request.POST.get('Autor')

        # Crear un nuevo post
        nuevo_post = Post(
            Titulo=titulo,
            Descripcion=descripcion,
            Imagen=imagen,
            Fecha=fecha if fecha else timezone.now().date(),
            Autor=autor
        )
        nuevo_post.save()

        for user in User.objects.all():
            Notificacion.objects.create(user=user, tipo='noticia', objeto_id=nuevo_post.id)


        # Agregar un mensaje de éxito
        messages.success(request, '¡Noticia creada exitosamente!')
        

        # Redirigir al formulario
        return redirect('noticias:crear_post')

    # Renderizar el formulario si el método no es POST
    return render(request, 'crear_post.html')
    # Renderizar el formulario si el método no es POST
    return render(request, 'crear_post.html')

@user_passes_test(lambda u: u.is_superuser)  # Restringir a superusuarios
def eliminar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, 'El post ha sido eliminado exitosamente.')
    return redirect('noticias:posts')  # Redirigir a la lista de posts


@login_required
@user_passes_test(lambda u: u.is_superuser)
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    comentario.delete()
    return redirect('noticias:post_detail', post_id=comentario.post.id)