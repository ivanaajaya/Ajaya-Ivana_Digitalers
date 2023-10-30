from django.urls import path, include

from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('servicios/', TipoServicioList.as_view(), name="servicios"),
    path('servicios/nuevo/', TipoServicioCreate.as_view(), name='nuevo-servicio'),
    path('servicios/actualizar/<int:pk>/', TipoServicioUpdate.as_view(), name="actualizar-servicio"),
    path('servicios/eliminar/<int:pk>/', TipoServicioDelete.as_view(), name="eliminar-servicio"),
    
    path('empleados/', EmpleadoList.as_view(), name="empleados"),
    
    path('registro/', RegistroView.as_view(), name="registro"),
    path('perfil/', perfil_view, name="perfil"),
    path('editar_perfil/', PerfilUpdateView.as_view(), name='editar_perfil'),
    path('editar_usuario/', EditProfileView.as_view(), name='editar_usuario'),
    path('login/', MyLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page="login"), name="logout"),
    
    path('reservas/nueva/<int:pk>', ReservaCreateView.as_view(), name='nueva-reserva'),
    path('reservas/', ReservasListView.as_view(), name='reservas_list'),
    path('reservas/actualizar/<int:pk>/', ReservaUpdateView.as_view(), name='actualizar-reserva'),
]