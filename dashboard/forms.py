from django import forms
from web.models import BudgetRequest, Service, GalleryImage, TeamMember, Video, ContactInfo, AboutUs, AboutImage


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Poda de árboles en altura'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe brevemente el servicio ofrecido...'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Trabajos realizados en zona norte'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Presentación de la empresa'
            }),
            'video_file': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = "__all__"
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contacto@empresa.cl'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Calle Los Robles #123, Melipilla'
            }),
        }


class AboutUsForm(forms.ModelForm):
    class Meta:
        model = AboutUs
        fields = "__all__"
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Cuenta la historia de la empresa, su misión y visión...'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

class AboutImageForm(forms.ModelForm):
    class Meta:
        model = AboutImage
        fields = "__all__"

class TeamMemberForm(forms.ModelForm):
    class Meta:
            model = TeamMember
            fields = "__all__"

class BudgetRequestForm(forms.ModelForm):
    class Meta:
        model = BudgetRequest
        fields = ['name', 'email', 'phone', 'comuna', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe brevemente el trabajo que necesitas...'}),
        }