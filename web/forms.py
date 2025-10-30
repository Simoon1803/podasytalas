from django import forms
from web.models import BudgetRequest

class BudgetRequestForm(forms.ModelForm):
    class Meta:
        model = BudgetRequest
        fields = ['name', 'email', 'phone', 'comuna', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe brevemente el trabajo que necesitas...'
            }),
        }


class ContactForm(forms.Form):
    name = forms.CharField(
        label="Nombre completo",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre completo'})
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tucorreo@ejemplo.com'})
    )
    phone = forms.CharField(
        label="Teléfono",
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 1234 5678'})
    )
    comuna = forms.CharField(
        label="Comuna",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu comuna'})
    )
    message = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escribe tu mensaje aquí...'})
    )