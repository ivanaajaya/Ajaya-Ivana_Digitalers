from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Importaciones de Modelos
from .models import Empleado, Cliente, TipoServicio,Reserva
from .forms import RegistroForm, EmpleadoForm, ClienteForm, UserEditForm, TipoServicioForm, ReservaUpdateForm, ReservaForm
from django.contrib.auth.models import User

# Importaciones de CBV
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from django.views.generic import FormView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic import DeleteView

# Create your views here.

# CLASS BASED VIEWS 
class HomeView(TemplateView):
    """para mostrar el iniciio de la pagina"""
    template_name = "miapp/home.html"

class MyLoginView(LoginView):
    """Vista personalizada para el inicio de sesión."""
    redirect_authenticated_user = True

    def get_success_url(self):#si es valido
        return reverse_lazy('home')

    def form_invalid(self, form):#si NO es valido
        messages.error(self.request, "Usuario o contraseña inválidos")
        return self.render_to_response(self.get_context_data(form=form))

class EmpleadoList(ListView):
    """Muestra una lista los Empleados"""
    model = Empleado
    
    def get_context_data(self, **kwargs):
        """sirve para el titulo"""
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = "Lista de los Empleados"
        return contexto
class TipoServicioList(ListView):
    """Muestra una lista de todos los Servicios y  hace la busqueda"""
    model = TipoServicio
    
    def get_queryset(self):
        queryset = TipoServicio.objects.all()
        search_term = self.request.GET.get('q')
        if search_term:
            # Filtra los servicios por nombres o descripcion
            queryset = queryset.filter(Q(nombreServicio__icontains=search_term) | Q(descripcion__icontains=search_term))
        return queryset
    
    def get_context_data(self, **kwargs):
        """sirve para el titulo"""
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = "Lista de Servicios"
        return contexto
    
class RegistroView(FormView):
    """Vista para el registro de usuarios."""
    template_name = 'miapp/registro.html'  # Crea esta plantilla para el formulario de registro
    form_class = RegistroForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Inicia sesión automáticamente después del registro
        
        #determina si es un empleado o cliente
        if form.cleaned_data['palabraClave'] == 'clave':
            Empleado.objects.create(usuario=user, nombreEmpleado=form.cleaned_data['nombre'], apellidoEmpleado=form.cleaned_data['apellido'], correoEmpleado=form.cleaned_data['correo'])
        else:
            Cliente.objects.create(usuario=user, nombreCliente=form.cleaned_data['nombre'], apellidoCliente=form.cleaned_data['apellido'], correoCliente=form.cleaned_data['correo'])
        return super().form_valid(form)
    
@login_required
def perfil_view(request):
    """Muestra el perfil del usuario (cliente o empleado)."""
    if hasattr(request.user, 'empleado'):
        return EmpleadoDetailView.as_view()(request)
    elif hasattr(request.user, 'cliente'):
        return ClienteDetailView.as_view()(request)
    else:
        return HttpResponseRedirect(reverse_lazy('home')) #No funciona

class EmpleadoDetailView(LoginRequiredMixin, DetailView):
    """Vista para mostrar el perfil de un Empleado."""
    model = Empleado
    template_name = 'miapp/empleado_perfil.html'
    context_object_name = 'perfil'

    def get_object(self, queryset=None):
        return self.request.user.empleado

class ClienteDetailView(LoginRequiredMixin, DetailView):
    """Vista para mostrar el perfil de un Cliente."""
    model = Cliente
    template_name = 'miapp/cliente_perfil.html'
    context_object_name = 'perfil'

    def get_object(self, queryset=None):
        return self.request.user.cliente
    
class PerfilUpdateView(UpdateView):
    """Vista para actualizar el perfil de un usuario (Empleado o Cliente)."""
    form_class = None
    template_name_suffix = "_update_form" 

    def get_model_and_form(self):
        # Determine si es un Empleado o un Cliente y asigna el modelo y el formulario.
        if hasattr(self.request.user, 'empleado'):
            self.model = Empleado
            self.form_class = EmpleadoForm
        elif hasattr(self.request.user, 'cliente'):
            self.model = Cliente
            self.form_class = ClienteForm

    def get_object(self, queryset=None):
        self.get_model_and_form()
        if self.model == Empleado:
            return self.request.user.empleado
        else:
            return self.request.user.cliente
        
    def get_success_url(self):
        return reverse_lazy('perfil') + "?ok"
    
class EditProfileView(LoginRequiredMixin, UpdateView):
    """Vista para editar el perfil del usuario."""
    model = User
    form_class = UserEditForm
    template_name = 'miapp/edit_profile.html'
    success_url = reverse_lazy('perfil')

    def get_object(self, queryset=None):
        return self.request.user
    
class TipoServicioCreate(CreateView):
    """Crea un nuevo servicio"""
    model = TipoServicio
    form_class = TipoServicioForm
    template_name = 'miapp/agregar_servicio.html'

    def get_success_url(self):
        return reverse_lazy('servicios')
    
class TipoServicioUpdate(UpdateView):
    """Vista para actualizar un Servicio."""
    model = TipoServicio
    form_class = TipoServicioForm
    template_name_suffix = "_update_form" 

    def get_success_url(self):
        return reverse_lazy('actualizar-servicio', args=[self.object.id])+"?ok"
    
class TipoServicioDelete(DeleteView):
    """Vista para eliminar un Servicio."""
    model = TipoServicio
    success_url = reverse_lazy('servicios')
    
class ReservasListView(LoginRequiredMixin, ListView):
    """Vista para mostrar la lista de reservas."""
    model = Reserva
    template_name = 'miapp/reservas_list.html'
    context_object_name = 'reservas'
    
    def get_queryset(self):
        #Obtiene y filtra las reservas (cliente o empleado) autenticado.
        if hasattr(self.request.user, 'cliente'):
            return Reserva.objects.filter(cliente=self.request.user.cliente)
        elif hasattr(self.request.user, 'empleado'):
            return Reserva.objects.filter(empleado=self.request.user.empleado)
        return reverse_lazy('home')  # No funciona
    
class ReservaUpdateView(UpdateView):
    """Vista para actualizar una reserva."""
    model = Reserva
    form_class = ReservaUpdateForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse_lazy('reservas_list')
    
class ReservaServicioView(CreateView):
    """Vista para reservar un turno."""
    model = Reserva
    form_class = ReservaForm
    template_name = 'miapp/reserva_servicio.html'
    success_url = reverse_lazy('reservas_list')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        servicio = get_object_or_404(TipoServicio, id=self.kwargs['servicio_id'])
        contexto['servicio'] = servicio
        return contexto

    def form_valid(self, form):
        form.instance.cliente = self.request.user.cliente
        servicio = get_object_or_404(TipoServicio, id=self.kwargs['servicio_id'])
        form.instance.empleado = form.cleaned_data['empleado']
        form.instance.tipoServicio = servicio
        return super().form_valid(form)
    
class IvanaAView(TemplateView):
    """Vista Acerca de mi"""
    template_name = "miapp/ivanaA.html"