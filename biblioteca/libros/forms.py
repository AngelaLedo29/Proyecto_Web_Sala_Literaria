from django import forms
from django.forms import ModelForm
from django_select2 import forms as s2forms

from . import models

# Crear formulario de contacto
class ContactoForm(forms.Form):
    ''' Contacto form '''
    email = forms.EmailField(required=True)
    asunto = forms.CharField(required=True)
    mensaje = forms.CharField(widget=forms.Textarea, required=True)
    email.widget.attrs.update({'class': 'form-control'})
    asunto.widget.attrs.update({'class': 'form-control'})
    mensaje.widget.attrs.update({'class': 'form-control'})

# Crear LibroForm
class AutorWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        'nombre__icontains',
        'apellidos__icontains',
    ]

class GeneroWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        'nombre__icontains',
    ]
    
class LibroForm(forms.ModelForm):
    class Meta:
        model = models.Libro
        fields = '__all__'
        widgets = {
            'autor': AutorWidget,
            'genero': GeneroWidget
        }