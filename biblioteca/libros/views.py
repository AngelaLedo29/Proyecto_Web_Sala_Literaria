from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from libros.models import Libro, Autor, Genero, Reseña, Usuario, ListaLectura
from libros.forms import ContactoForm
from . import models, forms

# Create your views here.
def home(request):
    # libros = Libro.objects.all()
    libros_actualidad = Libro.objects.filter(año_publicacion="2024")
    libros_literatura_erótica = Libro.objects.filter(genero__nombre="Literatura erótica")
    libros_realismo_mágico = Libro.objects.filter(genero__nombre="Realismo mágico")
    autores = Autor.objects.all()
    generos = Genero.objects.all()
    
    context = {
        'libros_actualidad': libros_actualidad,
        'libros_literatura_erótica': libros_literatura_erótica,
        'libros_realismo_mágico': libros_realismo_mágico,
        'autores': autores,
        'generos': generos
    }
    return render(request, "home.html", context)

# Listas Genericas de Libros
class LibroListView(ListView):
    '''Vista genérica para el listado de libros'''
    model = Libro
    # paginate_by = 15
    def get_queryset(self):
        return Libro.objects.all().order_by('titulo')
    
    def get_context_data(self, **kwargs):
        context = super(LibroListView, self).get_context_data(**kwargs)
        # context["ahora"] = datetime.datetime.now()
        return context
    
class LibroDetailView(DetailView):
    '''Vista genérica para el detalle de un libro'''
    model = Libro

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reseñas'] = self.object.reseña_set.all()
        return context

# Listas Genericas de Autores
class AutorListView(ListView):
    model = Autor
    # paginate_by = 15
    def get_queryset(self):
        return Autor.objects.all().order_by('apellidos')
    
    def get_context_data(self, **kwargs):
        context = super(AutorListView, self).get_context_data(**kwargs)
        # context["ahora"] = datetime.datetime.now()
        return context
    
class AutorDetailView(DetailView):
    model = Autor

# Listas Genericas de Géneros
class GeneroListView(ListView):
    model = Genero

    def get_queryset(self):
        return Genero.objects.all().order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super(GeneroListView, self).get_context_data(**kwargs)
        # context["ahora"] = datetime.datetime.now() 
        return context
    
class GeneroDetailView(DetailView):
    model = Genero

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genero = self.get_object()
        context['libro_list'] = genero.libro_set.all()
        return context

# Listas Genericas de Lista Lectura
class ListaLecturaListView(ListView):
    model = ListaLectura

    def get_queryset(self):
        return ListaLectura.objects.all().order_by('nombre')
    
    def get_context_data(self, **kwargs):
        context = super(ListaLecturaListView, self).get_context_data(**kwargs)
        # context["ahora"] = datetime.datetime.now() 
        return context
    
class ListaLecturaDetailView(DetailView):
    model = ListaLectura
    
# Busqueda de libros
class SearchResultsListViewLibro(ListView):
    model = Libro

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            self.query = query
            return Libro.objects.filter(titulo__icontains=query)
        else:
            return[]
    
    def get_context_data(self, **kwargs):
        context = super(SearchResultsListViewLibro, self).get_context_data(**kwargs)
        context['busqueda'] = self.query
        context['anterior'] = self.request.META.get('HTTP_REFERER')
        return context

class SearchResultsListViewAutor(ListView):
    model = Autor

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            self.query = query
            return Autor.objects.filter(nombre__icontains=query, apellidos__icontains=query)
        else:
            return[]
        
    def get_context_data(self, **kwargs):
        context = super(SearchResultsListViewAutor, self).get_context_data(**kwargs)
        context['buscar'] = self.query
        context['anterior'] = self.request.META.get('HTTP_REFERER')
        return context
    
# Formulario de contacto
def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            asunto = form.cleaned_data['asunto']
            mensaje = form.cleaned_data['mensaje']
            try:
                send_mail(asunto, mensaje, email, ['angelaledo29@gmail.com', email])
            except BadHeaderError:
                return HttpResponse('Se ha encontrado un encabezado no válido.')
            messages.success(request, 'Mensaje enviado correctamente')
            return HttpResponseRedirect(reverse('home'))
        messages.error(request, 'Error al enviar el mensaje')

    context = {'form': ContactoForm()}
    return render(request, 'contacto.html', context)

# Gestión de autores con vistas genéricas
class AutorCreate(CreateView):
    model = Autor
    fields = ['nombre', 'apellidos', 'biografia', 'nacionalidad']
    success_url = reverse_lazy('lista-autores')

class AutorUpdate(UpdateView):
    model = Autor
    fields = ['nombre', 'apellidos', 'biografia', 'nacionalidad']
    success_url = reverse_lazy('lista-autores')

class AutorDelete(DeleteView):
    model = Autor
    success_url = reverse_lazy('lista-autores')

# Gestión de libros con vistas genéricas
class LibroCreate(CreateView):
    model = Libro
    fields = '__all__'
    success_url = reverse_lazy('lista-libros')

class LibroUpdate(UpdateView):
    model = Libro
    fields = '__all__'
    success_url = reverse_lazy('lista-libros')

class LibroDelete(DeleteView):
    model = Libro
    success_url = reverse_lazy('lista-libros')

# Gestión de reseñas con vistas genéricas
class ReseñaCreate(CreateView):
    model = Reseña
    fields = '__all__'
    success_url = reverse_lazy('detalle-libro')

class ReseñaUpdate(UpdateView):
    model = Reseña
    fields = '__all__'
    success_url = reverse_lazy('detalle-libro')

class ReseñaDelete(DeleteView):
    model = Reseña
    success_url = reverse_lazy('detalle-libro')

# Gestión de usuarios con vistas genéricas
class UsuarioCreate(CreateView):
    model = Usuario
    fields = '__all__'
    success_url = reverse_lazy('home')

# Gestión de Lista de Lectura con vistas genéricas
class ListaLecturaCreate(CreateView):
    model = ListaLectura
    fields = '__all__'
    success_url = reverse_lazy('lista-lectura')

class ListaLecturaUpdate(UpdateView):
    model = ListaLectura
    fields = '__all__'
    success_url = reverse_lazy('lista-lectura')

class ListaLecturaDelete(DeleteView):
    model = ListaLectura
    success_url = reverse_lazy('lista-lectura')