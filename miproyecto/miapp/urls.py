from django.urls import path, include

from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('servicios/', TipoServicioList.as_view(), name="servicios"),
    path('empleados/', EmpleadoList.as_view(), name="empleados"),
    
    path('login/', MyLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page="login"), name="logout"),
]