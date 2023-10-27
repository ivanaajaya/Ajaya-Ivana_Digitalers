from django.contrib import admin
from .models import Usuario, Empleado, Cliente, Reserva

# Register your models here.
class UsuarioAdmin(admin.ModelAdmin):
    pass

class EmpleadoAdmin(admin.ModelAdmin):
    pass

class ClienteAdmin(admin.ModelAdmin):
    pass

class ReservaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Reserva, ReservaAdmin)