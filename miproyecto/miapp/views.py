from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect


# Importaciones de Modelos
from .models import Empleado, Cliente, TipoServicio,Reserva
from .forms import RegistroForm, EmpleadoForm, ClienteForm, UserEditForm, TipoServicioForm, ReservaUpdateForm
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
    
class RegistroView(FormView):
    template_name = 'miapp/registro.html'  # Crea esta plantilla para el formulario de registro
    form_class = RegistroForm
    success_url = reverse_lazy('login')  # Define la URL a la que se redirigirá después del registro

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Inicia sesión automáticamente después del registro
        # Aquí determina si es un empleado o cliente
        if form.cleaned_data['palabraClave'] == 'clave':
            Empleado.objects.create(usuario=user, nombreEmpleado=form.cleaned_data['nombre'], apellidoEmpleado=form.cleaned_data['apellido'], correoEmpleado=form.cleaned_data['correo'])
        else:
            Cliente.objects.create(usuario=user, nombreCliente=form.cleaned_data['nombre'], apellidoCliente=form.cleaned_data['apellido'], correoCliente=form.cleaned_data['correo'])
        return super().form_valid(form)
    

@login_required
def perfil_view(request):
    """muestra el perfil, clinte o empleado"""
    if hasattr(request.user, 'empleado'):
        return EmpleadoDetailView.as_view()(request)
    elif hasattr(request.user, 'cliente'):
        return ClienteDetailView.as_view()(request)
    else:
        # Maneja el caso en el que el usuario no tiene un perfil asociado
        # Puedes redirigirlo a una página de error o tomar alguna otra acción.
        # Por ejemplo, puedes redirigirlo a la página de inicio.
        return HttpResponseRedirect(reverse_lazy('home'))

class EmpleadoDetailView(LoginRequiredMixin, DetailView):
    model = Empleado
    template_name = 'miapp/empleado_perfil.html'
    context_object_name = 'perfil'

    def get_object(self, queryset=None):
        return self.request.user.empleado

class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'miapp/cliente_perfil.html'
    context_object_name = 'perfil'

    def get_object(self, queryset=None):
        return self.request.user.cliente
    
class PerfilUpdateView(UpdateView):
    form_class = None  # Debes asignar el formulario apropiado (EmpleadoForm o ClienteForm)
    template_name_suffix = "_update_form" 

    def get_model_and_form(self):
        # Determine si el usuario es un Empleado o un Cliente y asigna el modelo y el formulario correspondientes.
        if hasattr(self.request.user, 'empleado'):
            self.model = Empleado
            self.form_class = EmpleadoForm
        elif hasattr(self.request.user, 'cliente'):
            self.model = Cliente
            self.form_class = ClienteForm

    def get_object(self, queryset=None):
        self.get_model_and_form()  # Llamamos a la función para determinar el modelo y el formulario.
        # Devuelve el perfil del usuario autenticado
        if self.model == Empleado:
            return self.request.user.empleado
        else:
            return self.request.user.cliente
        
    def get_success_url(self):
        return reverse_lazy('perfil') + "?ok"
    
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'miapp/edit_profile.html'  # Crea una plantilla personalizada para la edición del perfil
    success_url = reverse_lazy('perfil')  # URL a la que redirigir después de la edición exitosa

    def get_object(self, queryset=None):
        return self.request.user
    
class TipoServicioCreate(CreateView):
    """Crea un nuevo servicio"""
    model = TipoServicio
    form_class = TipoServicioForm
    template_name = 'miapp/agregar_servicio.html'  # Elige el nombre de la plantilla que utilizarás para el formulario de creación

    def get_success_url(self):
        return reverse_lazy('servicios')  # Redirige a la lista de servicios después de crear uno
    
class TipoServicioUpdate(UpdateView):
    model = TipoServicio
    form_class = TipoServicioForm
    template_name_suffix = "_update_form" 

    def get_success_url(self):
        return reverse_lazy('actualizar-servicio', args=[self.object.id])+"?ok"
    
class TipoServicioDelete(DeleteView):
    model = TipoServicio
    success_url = reverse_lazy('servicios')
    
class ReservasListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'miapp/reservas_list.html'
    context_object_name = 'reservas'
    
    def get_queryset(self):
        if hasattr(self.request.user, 'cliente'):
            # Filtra las reservas del cliente actualmente autenticado
            return Reserva.objects.filter(cliente=self.request.user.cliente)
        elif hasattr(self.request.user, 'empleado'):
            # Filtra las reservas del empleado actualmente autenticado
            return Reserva.objects.filter(empleado=self.request.user.empleado)
        return Reserva.objects.none()  # Por si acaso no es ni cliente ni empleado
    
class ReservaUpdateView(UpdateView):
    model = Reserva
    form_class = ReservaUpdateForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse_lazy('reservas_list')  # Redirige a la lista de reservas después de editar una reserva
    
class ReservaCreateView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaUpdateForm  # Usa el mismo formulario que para la actualización
    template_name = 'miapp/reserva_create_form.html'  # Crea una plantilla para el formulario de creación

    def form_valid(self, form):
        form.instance.cliente = self.request.user.cliente  # Asigna el cliente actual
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('reservas_list')  # Redirige a la lista de reservas después de crear una reserva
