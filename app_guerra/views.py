from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app_guerra.models import Guerra, Enemigo, Perfil
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from .forms import MejoraForm
from .models import MejoraEdificio
from django.contrib.auth.decorators import login_required


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Perfil, Guerra
from .forms import EnemigoForm

@login_required
def vista_guerra_usuario(request):
    perfil = Perfil.objects.get(usuario=request.user)
    guerras_activas = Guerra.objects.filter(en_curso=True).order_by('-fecha_inicio')

    if request.method == 'POST':
        form = EnemigoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('guerras_usuario')  # Cambia por el nombre correcto de tu URL
    else:
        form = EnemigoForm()

    guerras_y_enemigos = []
    for guerra in guerras_activas:
        enemigos = guerra.enemigos.all()

        enemigos_info = []
        for enemigo in enemigos:
            segundos_restantes = enemigo.tiempo_restante() if not enemigo.ha_regenerado() else 0

            enemigos_info.append({
                'obj': enemigo,
                'segundos_restantes': segundos_restantes,
                'regenerado': enemigo.ha_regenerado()
            })

        enemigos_info.sort(key=lambda x: (not x['regenerado'], x['segundos_restantes']))

        guerras_y_enemigos.append({
            'guerra': guerra,
            'enemigos': enemigos_info
        })

    return render(request, 'usuarios/guerra_usuario.html', {
        'rango': perfil.rango,
        'guerras_y_enemigos': guerras_y_enemigos,
        'form': form,  # Ahora sí está definido y enviado
    })


@login_required
def vista_mejoras(request):
    perfil = Perfil.objects.get(usuario=request.user)

    # Mis mejoras
    mis_mejoras = MejoraEdificio.objects.filter(usuario=request.user).order_by('-fecha_inicio')
    mis_mejoras_info = [
        {'obj': mejora, 'segundos_restantes': int(mejora.tiempo_restante().total_seconds())}
        for mejora in mis_mejoras
    ]

    # Mejoras de otros
    mejoras_otros = MejoraEdificio.objects.exclude(usuario=request.user).order_by('-fecha_inicio')
    mejoras_otros_info = [
        {'obj': mejora, 'segundos_restantes': int(mejora.tiempo_restante().total_seconds())}
        for mejora in mejoras_otros
    ]

    # Registrar mejora
    if request.method == 'POST':
        form = MejoraForm(request.POST)
        if form.is_valid():
            nueva = form.save(commit=False)
            nueva.usuario = request.user
            if not nueva.fecha_inicio:
                nueva.fecha_inicio = timezone.now()
            nueva.save()
            return redirect('vista_mejoras')
    else:
        form = MejoraForm()

    return render(request, 'usuarios/mejoras.html', {
        'perfil': perfil,
        'mis_mejoras': mis_mejoras_info,
        'mejoras_otros': mejoras_otros_info,
        'form': form,
    })


# app_guerra/views.py
# Ya te lo mostré antes, pero confirmo que es igual:
import requests
from django.shortcuts import render
from datetime import datetime

def steam_news(request):
    appid = 1927780
    url = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/"
    params = {
        'appid': appid,
        'count': 5,
        'maxlength': 300,
        'format': 'json',
    }

    noticias = []
    try:
        response = requests.get(url, params=params)
        data = response.json()

        # Imprimir todo el JSON para inspección
        import json
        print(json.dumps(data, indent=4, ensure_ascii=False))

        noticias = data['appnews']['newsitems']

        for noticia in noticias:
            timestamp = noticia.get('date')
            if timestamp:
                from datetime import datetime
                noticia['fecha_formateada'] = datetime.fromtimestamp(timestamp)
            else:
                noticia['fecha_formateada'] = None

    except Exception as e:
        print("Error al obtener noticias de Steam:", e)
        noticias = []

    return render(request, 'usuarios/eventos.html', {'noticias': noticias})


from django.shortcuts import redirect, get_object_or_404
from .models import Enemigo
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

@login_required
def reiniciar_enemigo(request, enemigo_id):
    if request.method == "POST":
        enemigo = get_object_or_404(Enemigo, id=enemigo_id)
        enemigo.ultima_vez_atacado = timezone.now()
        enemigo.save()
        return redirect('guerras_usuario')  # o la vista que renderiza el template
    return redirect('guerras_usuario')
