from django.contrib import admin
from .models import Genero, Autor, Usuario, Libro, ListaLectura, Reseña
from django.utils.translation import gettext_lazy as _

# Register your models here.
# admin.site.register(Genero)
# admin.site.register(Autor)
# admin.site.register(Usuario)
# admin.site.register(Libro)
# admin.site.register(ListaLectura)
# admin.site.register(Reseña)

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'display_genero')
    list_filter = ('autor', 'genero')
    search_fields = ('titulo', 'autor__apellidos', 'autor__nombre', 'genero')

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('apellidos', 'nombre', 'biografia', 'nacionalidad')
    fields = ['nombre', 'apellidos', ('biografia', 'nacionalidad')]

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    pass

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email')

@admin.register(ListaLectura)
class ListaLecturaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario')

@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = ('libro', 'usuario', 'calificacion')