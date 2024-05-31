from django.db import models
from django.contrib import admin

# Create your models here.
class Genero(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    biografia = models.TextField()
    nacionalidad = models.CharField(max_length=100)

    def __str__(self):
         return '%s, %s' % (self.apellidos, self.nombre)
    
class Usuario(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre
    
class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey("Autor", on_delete=models.SET_NULL, null=True)
    sinopsis = models.TextField(help_text="Ingrese una breve descripción del libro")
    genero = models.ManyToManyField("Genero", help_text="Seleccione un genero para este libro")
    año_publicacion = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    portada = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.titulo
    
    def display_genero(self):
        return ', '.join(genero.nombre for genero in self.genero.all()[:3])
    
    display_genero.short_description = 'Genero'

class ListaLectura(models.Model):
    libros = models.ManyToManyField("Libro", related_name="listas_lectura")
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Reseña(models.Model):
    libro = models.ForeignKey("Libro", on_delete=models.CASCADE)
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)
    calificacion = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField()

    def __str__(self):
        return self.libro.titulo