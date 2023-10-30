from django.contrib import admin
from .models import Empleado, Cliente, Reserva, TipoServicio

# Register your models here.
class UsuarioAdmin(admin.ModelAdmin):
    pass

class EmpleadoAdmin(admin.ModelAdmin):
    pass

class ClienteAdmin(admin.ModelAdmin):
    pass

class ReservaAdmin(admin.ModelAdmin):
    pass

class TipoServicioAdmin(admin.ModelAdmin):
    pass


admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(TipoServicio, TipoServicioAdmin)
admin.site.register(Reserva, ReservaAdmin)