from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
from web.models import AboutImage, BudgetRequest, Service, GalleryImage, TeamMember, Video, ContactInfo, AboutUs
from .forms import AboutImageForm, ServiceForm, GalleryImageForm, TeamMemberForm, VideoForm, ContactInfoForm, AboutUsForm , BudgetRequestForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

# ----------------------------
# 🔹 INICIO DEL PANEL
# ----------------------------
@staff_member_required
def dashboard_home(request):
    total_servicios = Service.objects.count()
    total_imagenes = GalleryImage.objects.count()
    total_videos = Video.objects.count()
    return render(request, 'dashboard/home.html', {
        'total_servicios': total_servicios,
        'total_imagenes': total_imagenes,
        'total_videos': total_videos
    })


# ----------------------------
# 🔹 SERVICIOS
# ----------------------------
@staff_member_required
def service_list(request):
    services = Service.objects.all().order_by('-created_at')
    return render(request, "dashboard/service_list.html", {"services": services})


@staff_member_required
def service_add(request):
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Servicio creado correctamente")
            return redirect("dashboard:service_list")
        else:
            messages.error(request, "❌ Error al crear el servicio")
    else:
        form = ServiceForm()
    return render(request, "dashboard/service_form.html", {"form": form, "title": "Nuevo Servicio"})


@staff_member_required
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ Servicio actualizado correctamente")
            return redirect("dashboard:service_list")
        else:
            messages.error(request, "❌ Error al actualizar el servicio")
    else:
        form = ServiceForm(instance=service)
    return render(request, "dashboard/service_form.html", {"form": form, "title": "Editar Servicio"})


@staff_member_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    messages.success(request, "🗑️ Servicio eliminado correctamente")
    return redirect("dashboard:service_list")


# ----------------------------
# 🔹 GALERÍA
# ----------------------------
@staff_member_required
def gallery_list(request):
    """Lista de imágenes de la galería."""
    gallery = GalleryImage.objects.all().order_by('-created_at')
    return render(request, "dashboard/gallery_list.html", {"gallery": gallery})


@staff_member_required
def gallery_add(request):
    """Agregar una nueva imagen a la galería."""
    if request.method == "POST":
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Imagen agregada a la galería correctamente")
            return redirect("dashboard:gallery_list")
        else:
            messages.error(request, "❌ Error al agregar la imagen. Revisa los campos e inténtalo nuevamente.")
    else:
        form = GalleryImageForm()
    return render(request, "dashboard/gallery_form.html", {"form": form, "title": "Nueva Imagen"})


@staff_member_required
def gallery_edit(request, pk):
    """Editar una imagen existente de la galería."""
    image = get_object_or_404(GalleryImage, pk=pk)
    if request.method == "POST":
        form = GalleryImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            messages.success(request, "🖼️ Imagen actualizada correctamente")
            return redirect("dashboard:gallery_list")
        else:
            messages.error(request, "❌ Error al actualizar la imagen. Verifica los campos.")
    else:
        form = GalleryImageForm(instance=image)
    return render(request, "dashboard/gallery_form.html", {"form": form, "title": "Editar Imagen"})


@staff_member_required
def gallery_delete(request, pk):
    """Eliminar una imagen de la galería."""
    image = get_object_or_404(GalleryImage, pk=pk)
    image.delete()
    messages.success(request, "🗑️ Imagen eliminada correctamente")
    return redirect("dashboard:gallery_list")

# ----------------------------
# 🔹 VIDEOS
# ----------------------------
@staff_member_required
def video_list(request):
    videos = Video.objects.all().order_by('-created_at')
    return render(request, "dashboard/video_list.html", {"videos": videos})


@staff_member_required
def video_add(request):
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)  # 👈 AGREGA request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Video subido correctamente")
            return redirect("dashboard:video_list")
        else:
            messages.error(request, "❌ Error al subir el video")
    else:
        form = VideoForm()
    return render(request, "dashboard/video_form.html", {"form": form, "title": "Nuevo Video"})


@staff_member_required
def video_edit(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES, instance=video)  # 👈 también aquí
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ Video actualizado correctamente")
            return redirect("dashboard:video_list")
        else:
            messages.error(request, "❌ Error al actualizar el video")
    else:
        form = VideoForm(instance=video)
    return render(request, "dashboard/video_form.html", {"form": form, "title": "Editar Video"})


@staff_member_required
def video_delete(request, pk):
    video = get_object_or_404(Video, pk=pk)
    video.delete()
    messages.success(request, "🗑️ Video eliminado correctamente")
    return redirect("dashboard:video_list")


# ----------------------------
# 🔹 QUIÉNES SOMOS
# ----------------------------
@staff_member_required
def about_list(request):
    """Muestra la información de la empresa y sus imágenes."""
    about = AboutUs.objects.first()
    images = about.images.all() if about else []
    return render(request, "dashboard/about_list.html", {
        "about": about,
        "images": images
    })


@staff_member_required
def about_add(request):
    """Agrega información de la empresa."""
    if request.method == "POST":
        form = AboutUsForm(request.POST)
        if form.is_valid():
            about = form.save()
            messages.success(request, "✅ Información agregada correctamente")
            return redirect("dashboard:about_list")
        else:
            messages.error(request, "❌ Error al guardar la información")
    else:
        form = AboutUsForm()
    return render(request, "dashboard/about_form.html", {"form": form})


@staff_member_required
def about_edit(request, pk):
    """Edita la información de la empresa."""
    about = get_object_or_404(AboutUs, pk=pk)
    if request.method == "POST":
        form = AboutUsForm(request.POST, instance=about)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Información actualizada correctamente")
            return redirect("dashboard:about_list")
        else:
            messages.error(request, "❌ No se pudo actualizar la información")
    else:
        form = AboutUsForm(instance=about)
    return render(request, "dashboard/about_form.html", {"form": form})


@staff_member_required
def aboutimage_add(request):
    """Sube nuevas imágenes a Quiénes Somos."""
    if request.method == "POST":
        form = AboutImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Imagen agregada correctamente")
            return redirect("dashboard:about_list")
        else:
            messages.error(request, "❌ Error al subir la imagen")
    else:
        form = AboutImageForm()
    return render(request, "dashboard/aboutimage_form.html", {"form": form, "title": "Nueva Imagen"})

# 🔹 Eliminar imagen de Quiénes Somos
@staff_member_required
def aboutimage_delete(request, pk):
    image = get_object_or_404(AboutImage, pk=pk)
    image.delete()
    messages.success(request, "🗑️ Imagen eliminada correctamente")
    return redirect("dashboard:about_list")



# ----------------------------
# 🔹 CERRAR SESIÓN
# ----------------------------
@staff_member_required
def logout_view(request):
    logout(request)
    return redirect("/admin/login/")


# ----------------------------
# 🔹 EQUIPO DE TRABAJO
# ----------------------------
@staff_member_required
def team_list(request):
    about = AboutUs.objects.first()
    team = TeamMember.objects.filter(about=about) if about else []
    return render(request, "dashboard/team_list.html", {"team": team, "about": about})


@staff_member_required
def team_add(request):
    if request.method == "POST":
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Miembro agregado correctamente")
            return redirect("dashboard:team_list")
        else:
            messages.error(request, "❌ Error al guardar el miembro del equipo")
    else:
        form = TeamMemberForm()
    return render(request, "dashboard/team_form.html", {"form": form, "title": "Nuevo Miembro del Equipo"})


@staff_member_required
def team_edit(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == "POST":
        form = TeamMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ Miembro actualizado correctamente")
            return redirect("dashboard:team_list")
        else:
            messages.error(request, "❌ Error al actualizar los datos")
    else:
        form = TeamMemberForm(instance=member)
    return render(request, "dashboard/team_form.html", {"form": form, "title": "Editar Miembro"})


@staff_member_required
def team_delete(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    member.delete()
    messages.success(request, "🗑️ Miembro eliminado correctamente")
    return redirect("dashboard:team_list")


# --- Presupuestos ---
@staff_member_required
def budget_list(request):
    budgets = BudgetRequest.objects.all()
    return render(request, "dashboard/budget_list.html", {"budgets": budgets})


@staff_member_required
def budget_delete(request, pk):
    budget = get_object_or_404(BudgetRequest, pk=pk)
    budget.delete()
    messages.success(request, "🗑️ Solicitud eliminada correctamente.")
    return redirect("dashboard:budget_list")


def enviar_email_reset_password(request, user):
    """Envía un correo HTML bonito para restablecer contraseña"""
    subject = "Restablecer contraseña — Podas y Talas Isaías"
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]

    # Genera el enlace dinámico
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_url = f"http://{request.get_host()}/reset/{uid}/{token}/"

    # Renderiza tu plantilla HTML
    html_content = render_to_string("registration/password_reset_email.html", {
        "user": user,
        "reset_url": reset_url,
    })

    # Crea el correo y adjunta HTML
    msg = EmailMultiAlternatives(subject, "", from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()