from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.iniciar_sesion, name='login'),
        path('registro/', views.registro, name='registro'),  # 👈 ESTE ES CLAVE
        path('perfil/', views.perfil, name='perfil'),  # <-- esta línea es clave
        path('cerrar/', views.cerrar_sesion, name='cerrar_sesion'),



    # ... otras rutas si las tienes
]
