from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def usuarios (request):
    return HttpResponse ("APP USUARIOS") #Retornamos un mensaje de prueba

