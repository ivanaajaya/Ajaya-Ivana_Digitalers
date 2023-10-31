from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from ckeditor.widgets import CKEditorWidget

from .models import Cliente, Empleado, TipoServicio, Reserva

class RegistroForm(UserCreationForm):
    """Formulario de registro de usuario con validación de palabra clave para empleados."""
    nombre = forms.CharField(max_length=100, label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    apellido = forms.CharField(max_length=100, label='Apellido', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}))
    correo = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}))
    palabraClave = forms.CharField(max_length=15, required=False, label='¿Eres un Empleado? Ingresa la palabra clave', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Palabra clave'}))

    class Meta:
        model = User
        fields = ['username', 'nombre', 'apellido', 'correo', 'password1', 'password2']

    def clean_palabraClave(self):
        clave = self.cleaned_data['palabraClave']
        if clave != 'clave' and clave != '':  # Reemplaza 'clave' con tu palabra clave real
            raise ValidationError("---------LA PALABRA CLAVE NO ES CORRECTA---------si no eres un empleado deja vacio este campo-------------")
        return clave

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['correo']
        if commit:
            user.save()
        return user
    
class EmpleadoForm(forms.ModelForm):
    """Formulario para agregar y editar empleados."""
    class Meta:
        model = Empleado
        fields = ['nombreEmpleado', 'apellidoEmpleado', 'correoEmpleado', 'telefonoEmpleado', 'direccionEmpleado', 'horarioTrabajo', 'estadoEmpleo', 'numeroEmpleado', 'fotoEmpleado']
        widgets = {
            'nombreEmpleado': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidoEmpleado': forms.TextInput(attrs={'class': 'form-control'}),
            'correoEmpleado': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefonoEmpleado': forms.TextInput(attrs={'class': 'form-control'}),
            'direccionEmpleado': forms.TextInput(attrs={'class': 'form-control'}),
            'horarioTrabajo': forms.TextInput(attrs={'class': 'form-control'}),
            'estadoEmpleo': forms.Select(attrs={'class': 'form-control'}),
            'numeroEmpleado': forms.TextInput(attrs={'class': 'form-control'}),
            'fotoEmpleado': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        
class ClienteForm(forms.ModelForm):
    """Formulario para agregar y editar clientes."""
    class Meta:
        model = Cliente
        fields = ['nombreCliente', 'apellidoCliente', 'correoCliente', 'telefonoCliente', 'direccionCliente', 'fotoCliente']
        widgets = {
            'nombreCliente': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidoCliente': forms.TextInput(attrs={'class': 'form-control'}),
            'correoCliente': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefonoCliente': forms.TextInput(attrs={'class': 'form-control'}),
            'direccionCliente': forms.TextInput(attrs={'class': 'form-control'}),
            'fotoCliente': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        
class UserEditForm(forms.ModelForm):
    """Formulario para editar información de usuario."""
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        
class TipoServicioForm(forms.ModelForm):
    """Formulario para agregar y editar tipos de servicio."""
    class Meta:
        model = TipoServicio
        fields = ['nombreServicio', 'descripcion', 'imagen', 'duracionEstimada', 'costoEstimado']
        
        widgets = {
            'nombreServicio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Servicio'}),
            'descripcion': CKEditorWidget(),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'duracionEstimada': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Duración Estimada'}),
            'costoEstimado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Costo Estimado'}),
        }

        labels = {
            'nombreServicio': "",
            'description': ""
        }
        
class ReservaUpdateForm(forms.ModelForm):
    """Formulario para actualizar información de reservas."""
    class Meta:
        model = Reserva
        fields = ['empleado', 'fechaHora', 'direccionCliente', 'tipoServicio', 'estadoReserva']

    empleado = forms.ModelChoiceField(
        queryset=Empleado.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True  # siempre selecciona un empleado
    )

    fechaHora = forms.DateTimeField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 2023-10-29 12:00'}),
    )

    direccionCliente = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección del Cliente'}),
    )

    tipoServicio = forms.ModelChoiceField(
        queryset=TipoServicio.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    estadoReserva = forms.ChoiceField(
        choices=Reserva.ESTADO_RESERVA_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

class ReservaForm(forms.ModelForm):
    """Formulario para crear y editar reservas de servicios."""
    class Meta:
        model = Reserva
        fields = ['empleado', 'fechaHora', 'direccionCliente']
        widgets = {
            'fechaHora': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 2023-10-29 12:00'}),
            'direccionCliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección del Cliente'}),
        }

    empleado = forms.ModelChoiceField(
        queryset=Empleado.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True  # siempre selecciona un empleado
    )