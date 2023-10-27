from django.db import models
from django.contrib import admin

# Modelo para Usuarios
class Usuario(models.Model):
    """maneja la autenticación y el rol de los usuarios"""
    Nombre = models.CharField(max_length=100)
    CorreoElectronico = models.EmailField(unique=True)
    Contrasena = models.CharField(max_length=128)  # Aquí deberías almacenar el hash de la contraseña
    FotoPerfil = models.ImageField(upload_to="perfiles/", null=True, blank=True)
    FechaCreacion = models.DateTimeField(auto_now_add=True)
    UltimoIngreso = models.DateTimeField(auto_now=True)
    ROLES = (
        ('administrador', 'Administrador'),
        ('empleado', 'Empleado'),
        ('cliente', 'Cliente'),
    )
    Rol = models.CharField(max_length=20, choices=ROLES)
    
    # def __str__(self):
    #     return self.UsuarioID.Nombre

# Modelo para Empleados
class Empleado(models.Model):
    """almacenan información adicional sobre empleados"""
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    Nombre = models.CharField(max_length=100)
    Apellido = models.CharField(max_length=100)
    NumeroTelefono = models.CharField(max_length=15)
    Direccion = models.CharField(max_length=200)
    HorarioTrabajo = models.CharField(max_length=100)
    ESTADO_EMPLEO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('descanso', 'En Descanso'),
    )
    EstadoEmpleo = models.CharField(max_length=10, choices=ESTADO_EMPLEO_CHOICES)
    NumeroEmpleado = models.CharField(max_length=20, unique=True)
    
    # def __str__(self):
    #     return self.UsuarioID.Nombre

# Modelo para Clientes
class Cliente(models.Model):
    """almacenan información adicional sobre clientes"""
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    Nombre = models.CharField(max_length=100)
    Apellido = models.CharField(max_length=100)
    Direccion = models.CharField(max_length=200)
    NumeroTelefono = models.CharField(max_length=15)
    
    # Comentarios = models.TextField()
    
    # Si tengo tiempo:
    # un modelo de historial de reservas
    # para rastrear las reservas anteriores del cliente
    # HistorialReservas = models.ManyToManyField('Reserva', related_name='reservas_del_cliente')
    
    # def __str__(self):
    #     return self.UsuarioID.Nombre

# Modelo para Reservas de Servicios
class Reserva(models.Model):
    """registra la información de las reservas de servicios"""
    ReservaID = models.AutoField(primary_key=True)
    Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    Empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    FechaHora = models.DateTimeField()
    DireccionCliente = models.CharField(max_length=200)
    TipoServicio = models.CharField(max_length=100)
    DuracionEstimada = models.DurationField()
    ESTADO_RESERVA_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    )
    EstadoReserva = models.CharField(max_length=20, choices=ESTADO_RESERVA_CHOICES)
    CostoEstimado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    NumeroConfirmacion = models.CharField(max_length=20, unique=True, null=True, blank=True)


    # def __str__(self):
    #     return f"ReservaID: {self.ReservaID}, Cliente: {self.ClienteID.UsuarioID.Nombre}, Empleado: {self.EmpleadoID.UsuarioID.Nombre}"

