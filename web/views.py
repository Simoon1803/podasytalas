from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from web.forms import BudgetRequestForm, ContactForm
from web.models import Service, GalleryImage, Video, TeamMember, ContactInfo, AboutUs


def home(request):
    services = Service.objects.all()[:6]
    gallery = GalleryImage.objects.all()[:6]
    videos = list(Video.objects.all())

    team = TeamMember.objects.all()
    contact = ContactInfo.objects.first()
    about = AboutUs.objects.first()

    if request.method == "POST":
        form = BudgetRequestForm(request.POST, request.FILES)
        if form.is_valid():
            budget = form.save()

            context = {
                "name": budget.name,
                "email": budget.email,
                "phone": budget.phone,
                "comuna": budget.comuna,
                "description": budget.description,
                "image_url": request.build_absolute_uri(budget.image.url) if budget.image else None,
                "year": timezone.now().year,
            }

                        # Enviar correo al admin
            html_admin = render_to_string("emails/admin_notification.html", context)
            email_admin = EmailMultiAlternatives(
                subject=f"📋 Nueva solicitud de presupuesto — {budget.name}",
                body="Tienes una nueva solicitud de presupuesto.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=["isaiaspodasytalas@gmail.com"],
                reply_to=[budget.email],  # 👈 este es el cambio importante
            )
            email_admin.attach_alternative(html_admin, "text/html")
            email_admin.send()
            # Enviar confirmación al cliente
            html_client = render_to_string("emails/client_confirmation.html", context)
            email_client = EmailMultiAlternatives(
                subject="✅ Hemos recibido tu solicitud — Podas y Talas Isaías",
                body="Gracias por tu solicitud. Nos pondremos en contacto pronto.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[budget.email],
            )
            email_client.attach_alternative(html_client, "text/html")
            email_client.send()

            messages.success(request, "✅ Tu solicitud fue enviada correctamente.")
            return redirect("web:home")
        else:
            messages.error(request, "❌ Error al enviar la solicitud. Revisa los campos.")
    else:
        form = BudgetRequestForm()

    return render(request, "web/home.html", {
        "form": form,
        "services": services,
        "gallery": gallery,
        "videos": videos,
        "team": team,
        "contact": contact,
        "about": about,
    })


def contacto(request):
    return render(request, 'web/contacto.html')

def quienes_somos(request):
    """
    Vista para mostrar la información de la empresa, su historia, misión, visión, valores,
    galería y equipo de trabajo. Todo se carga automáticamente desde el panel administrador.
    """
    about = AboutUs.objects.prefetch_related('images', 'team_members').first()  # obtiene el primer registro de "about"
    context = {
        'about': about,
    }
    return render(request, 'web/quienes_somos.html', context)


def galeria(request):
    images = list(GalleryImage.objects.all())
    videos = list(Video.objects.all())

    combined = []
    max_len = max(len(images), len(videos))
    for i in range(max_len):
        if i < len(images):
            combined.append({'type': 'image', 'file': images[i]})
        if i < len(videos):
            combined.append({'type': 'video', 'file': videos[i]})

    return render(request, 'web/galeria.html', {'combined': combined})


def servicios(request):
    services = Service.objects.all().order_by('-id')
    return render(request, 'web/servicios.html', {'services': services})