
from django.urls import path
from . import views
from app_guerra.views import vista_guerra_usuario, vista_mejoras


urlpatterns = [
    path('guerras/', vista_guerra_usuario, name='guerras_usuario'),
    path('mejoras/', vista_mejoras, name='vista_mejoras'),
    path('steam-news/', views.steam_news, name='steam_news'),
    path('reiniciar-enemigo/<int:enemigo_id>/', views.reiniciar_enemigo, name='reiniciar_enemigo'),




]
