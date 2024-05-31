import json
from libros.models import Genero, Autor, Libro

url = 'libros.json'
with open(url, encoding='utf-8') as f:
    libros = json.load(f)

for libro in libros:
    autor = Autor.objects.filter(nombre=libro['autor'])
    if autor:
        autor = autor[0]
    else:
        autor = Autor.objects.create(nombre=libro['autor'])

    genero = Genero.objects.filter(nombre=libro['genero'])
    if genero:
        genero = genero[0]
    else:
        genero = Genero.objects.create(nombre=libro['genero'])

    l = Libro()
    if libro.get('titulo'):
        l.titulo = libro['titulo']
    
    if libro.get('autor'):
        l.autor = autor

    if libro.get('sinopsis'):
        l.sinopsis = libro['sinopsis']
    
    if libro.get('genero'):
        l.genero = genero

    if libro.get('año_publicacion'):
        l.año_publicacion = libro['año_publicacion']
    
    if libro.get('precio'):
        l.precio = libro['precio']

    if libro.get('portada'):
        portada = libro['portada']
        if portada.startswith('http'):
            l.portada = libro['portada']

    l.save()