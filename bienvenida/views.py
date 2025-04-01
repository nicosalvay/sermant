from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index (request):
    #Creamos un diccionario
    params = {}
    params ['nombre_sitio'] = 'Pagina Bienvenida'
    return render (request, 'bienvenida/index.html',params)
