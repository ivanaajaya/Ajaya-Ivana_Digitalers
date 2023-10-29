from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy

# Importaciones de Modelos
from .models import Usuario, Empleado, Cliente, TipoServicio,Reserva

# Importaciones de CBV
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from django.views.generic import FormView


# Create your views here.
# CLASS BASED VIEWS 
class HomeView(TemplateView):
    """para mostrar el iniciio de la pagina"""
    template_name = "miapp/home.html"

class MyLoginView(LoginView):
    redirect_authenticated_user = True #redirigirá a los usuarios ya autenticados a la URL especificada en "get_success_url"

    def get_success_url(self):#si es valido
        return reverse_lazy('home')

    def form_invalid(self, form):#si NO es valido
        messages.error(self.request, "Usuario o contraseña inválidos")
        return self.render_to_response(self.get_context_data(form=form))

class EmpleadoList(ListView):
    """Muestra todos los Empleados"""
    model = Empleado
    
    def get_context_data(self, **kwargs):
        """sirve para el titulo"""
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = "Lista de los Empleados"
        return contexto
class TipoServicioList(ListView):
    """Muestra todos los Servicios"""
    model = TipoServicio
    
    def get_context_data(self, **kwargs):
        """sirve para el titulo"""
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = "Lista de Servicios"
        return contexto