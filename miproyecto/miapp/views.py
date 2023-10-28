from django.shortcuts import render

# Importaciones de Modelos
from .models import Usuario, Empleado, Cliente, TipoServicio,Reserva

# Importaciones de CBV

from django.views.generic import TemplateView
from django.views.generic import ListView

# Create your views here.
class HomeView(TemplateView):
    """para mostrar el iniciio de la pagina"""
    template_name = "miapp/home.html"
