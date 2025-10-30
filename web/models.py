from django.db import models


# ---------------------------
# 🔹 SERVICIOS
# ---------------------------
class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título del servicio")
    description = models.TextField(verbose_name="Descripción")
    image = models.ImageField(upload_to="services/", verbose_name="Imagen del servicio")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# ---------------------------
# 🔹 GALERÍA GENERAL
# ---------------------------
class GalleryImage(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name="Título de la imagen")
    image = models.ImageField(upload_to="gallery/", verbose_name="Imagen")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Imagen de galería"
        verbose_name_plural = "Galería de imágenes"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title if self.title else f"Imagen {self.id}"


# ---------------------------
# 🔹 VIDEOS
# ---------------------------
class Video(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título del video")
    video_file = models.FileField(upload_to='videos/', verbose_name="Archivo de video")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# ---------------------------
# 🔹 CONTACTO
# ---------------------------
class ContactInfo(models.Model):
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    email = models.EmailField(verbose_name="Correo electrónico")
    address = models.CharField(max_length=255, verbose_name="Dirección")
    facebook = models.URLField(blank=True, null=True, verbose_name="Facebook")
    instagram = models.URLField(blank=True, null=True, verbose_name="Instagram")

    class Meta:
        verbose_name = "Información de contacto"
        verbose_name_plural = "Información de contacto"

    def __str__(self):
        return "Información de contacto"


# ---------------------------
# 🔹 QUIÉNES SOMOS
# ---------------------------
class AboutUs(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título principal")
    content = models.TextField(verbose_name="Descripción / Historia / Misión de la empresa")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Información de la empresa"
        verbose_name_plural = "Quiénes Somos"

    def __str__(self):
        return self.title


class AboutImage(models.Model):
    about = models.ForeignKey(
        AboutUs,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Sección relacionada"
    )
    image = models.ImageField(upload_to="about/", verbose_name="Imagen de la empresa")
    caption = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Descripción de la imagen (opcional)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Imagen de Quiénes Somos"
        verbose_name_plural = "Imágenes de Quiénes Somos"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Imagen de {self.about.title}"

class TeamMember(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre completo")
    role = models.CharField(max_length=100, verbose_name="Cargo o función")
    photo = models.ImageField(upload_to="team/", verbose_name="Foto del miembro")
    about = models.ForeignKey(
        AboutUs, on_delete=models.CASCADE, related_name="team_members", verbose_name="Empresa relacionada"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Miembro del equipo"
        verbose_name_plural = "Equipo de trabajo"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.role})"

class BudgetRequest(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre completo")
    email = models.EmailField(verbose_name="Correo electrónico")
    phone = models.CharField(max_length=20, verbose_name="Teléfono de contacto")
    comuna = models.CharField(max_length=100, verbose_name="Comuna")
    description = models.TextField(verbose_name="Descripción del trabajo")
    image = models.ImageField(upload_to="budgets/", blank=True, null=True, verbose_name="Imagen opcional")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Solicitud de presupuesto"
        verbose_name_plural = "Solicitudes de presupuestos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.comuna}"