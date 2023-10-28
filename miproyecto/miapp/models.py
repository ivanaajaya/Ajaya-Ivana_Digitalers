from django.db import models
from django.contrib import admin


# Modelo para Usuarios
class Usuario(models.Model):
    """maneja la autenticación y el rol de los usuarios"""
    usuario = models.CharField(max_length=100)
    correoElectronico = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)  # Aquí deberías almacenar el hash de la contraseña
    fotoPerfil = models.ImageField(upload_to="perfiles/", null=True, blank=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    ultimoIngreso = models.DateTimeField(auto_now=True)
    ROLES = (
        ('administrador', 'Administrador'),
        ('empleado', 'Empleado'),
        ('cliente', 'Cliente'),
    )
    rol = models.CharField(max_length=20, choices=ROLES)
    
    def __str__(self):
        return self.usuario

# Modelo para Empleados
class Empleado(models.Model):
    """almacenan información adicional sobre empleados"""
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombreEmpleado = models.CharField(max_length=100)
    apellidoEmpleado = models.CharField(max_length=100)
    numeroTelefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=200)
    horarioTrabajo = models.CharField(max_length=20) #ejemplo "9:00 AM - 5:00 PM"
    ESTADO_EMPLEO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('descanso', 'En Descanso'),
    )
    estadoEmpleo = models.CharField(max_length=10, choices=ESTADO_EMPLEO_CHOICES, default='activo')
    numeroEmpleado = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"{self.nombreEmpleado}, {self.apellidoEmpleado}"

# Modelo para Clientes
class Cliente(models.Model):
    """almacenan información adicional sobre clientes"""
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombreCliente = models.CharField(max_length=100)
    apellidoCliente = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    numeroTelefono = models.CharField(max_length=15)
    
    # Comentarios = models.TextField()
    
    # Si tengo tiempo:
    # un modelo de historial de reservas
    # para rastrear las reservas anteriores del cliente
    # HistorialReservas = models.ManyToManyField('Reserva', related_name='reservas_del_cliente')
    
    def __str__(self):
        return f"{self.nombreCliente}, {self.apellidoCliente}"

class TipoServicio(models.Model):
    nombreServicio = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="tipos_de_servicio/", null=True, blank=True)
    duracionEstimada = models.DurationField()

    def __str__(self):
        return self.nombreServicio

# Modelo para Reservas de Servicios
class Reserva(models.Model):
    """registra la información de las reservas de servicios"""
    numeroReserva = models.AutoField(primary_key=True, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fechaHora = models.DateTimeField()
    direccionCliente = models.CharField(max_length=200) #para confirmar la direcciondel cliente
    tipoServicio = models.ForeignKey(TipoServicio, on_delete=models.CASCADE)
    ESTADO_RESERVA_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    )
    estadoReserva = models.CharField(max_length=20, choices=ESTADO_RESERVA_CHOICES)
    costoEstimado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # numeroConfirmacion = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return f"Reserva: {self.numeroReserva}, Cliente: {self.cliente}, Empleado: {self.empleado}"


