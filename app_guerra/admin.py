from django.contrib import admin
from .models import Perfil, Guerra, MiembroAlianza, Enemigo, MejoraEdificio

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rango')
    list_filter = ('rango',)

@admin.register(Guerra)
class GuerraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'alianza_enemiga', 'en_curso', 'fecha_inicio')
    list_filter = ('en_curso',)

@admin.register(MiembroAlianza)
class MiembroAlianzaAdmin(admin.ModelAdmin):
    list_display = ('nombre_jugador', 'guerra', 'observaciones')

@admin.register(Enemigo)
class EnemigoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'coordenadas', 'guerra', 'ultima_vez_atacado')
    search_fields = ('nombre', 'coordenadas')


@admin.register(MejoraEdificio)
class MejoraEdificioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'categoria', 'edificio', 'nivel_inicial', 'nivel_objetivo', 'fecha_inicio', 'duracion_horas', 'planeta_principal', 'numero_colonia')
    list_filter = ('categoria', 'planeta_principal')
    search_fields = ('usuario__username', 'edificio')

from .models import MiembroAlianzaPropia

@admin.register(MiembroAlianzaPropia)
class MiembroAlianzaPropiaAdmin(admin.ModelAdmin):
    list_display = ['guerra', 'perfil', 'observaciones']
