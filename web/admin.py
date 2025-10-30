from django.contrib import admin
from web.models import Service, GalleryImage, Video, ContactInfo, AboutUs
from django.utils.html import format_html

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_preview', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)

    # 👇 Esto muestra una miniatura del video en el panel admin
    def video_preview(self, obj):
        if obj.video_file:  # usamos el nuevo campo
            return format_html(
                '<video width="200" controls><source src="{}" type="video/mp4"></video>',
                obj.video_file.url
            )
        return "—"
    video_preview.short_description = "Vista previa"

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'address')
    search_fields = ('phone', 'email', 'address')

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'content')
